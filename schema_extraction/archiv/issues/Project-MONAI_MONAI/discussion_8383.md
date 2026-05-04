# Discussion #8383: How to make tiffs where ITK from monai knows the pixel size?
**Repository:** Project-MONAI/MONAI
**Author:** joaomamede
**Created At:** 2025-03-10T20:50:30Z

## Description
Hi,

I have a pipeline from fluorescence microscopy that is working very well. I want to generalize it to different magnifications and microscopes and I am a bit stuck into making the input and ground truths DataSet() have the metadata for pixel size (X,Y,Z) be read from the tiff. This to pass it to the dataset dictionaries to transform it with SpacindD(). 
Here, I want tiff because it's the most common used format, and also to read it directly from the raw metadata to avoid data duplication (for example with bioio). For the inference I basically need a overall method that would work without LoadImaging through monai and I would just pass the pytorch tensor to the transforms.

Right now, for training model purposes I basically have my input and ground truths in nii.gz where I basically make it with this function, this works:
```
def save_nii(data, filepath, dtype, pixel_size):
    """Save data as a NIfTI file (XYZ format) with pixel size metadata."""
    affine = np.diag([pixel_size[2], pixel_size[1], pixel_size[0], 1])  # Ensure XYZ order
    img = nib.Nifti1Image(data.astype(dtype), affine=affine)
    img.header['pixdim'][1:4] = pixel_size  # Update voxel sizes
    img.header['xyzt_units'] = 2  # Microns (spatial units)
    nib.save(img, filepath)
```

I have an option to save the tiff, I tried different metadata passes to tifffile but nothing seems to work:
```
def save_tiff(data, filepath, dtype, pixel_size):
    """Save data as a TIFF file (ZYX format) with correct metadata for ITK."""
    metadata = {
        "spacing": pixel_size,  # Ensure spacing is stored correctly
        "spacing_units": "microns",
        "axes": "ZYX"
    }
    tiff.imwrite(filepath, data.astype(dtype), compression="lzw", metadata=metadata)
```

So, question #1 is how can I write the tiffs so that ITK/Monai have the pixel_size_x and pixel_size_z (these are 3d Z-stacks) properly read?


Question #2 how can I transform an array directly and pass the metadata for pixel_size_x to the monai.Data.DataSet class?
Right now I'm doing the production inference like this, what I need from this is an adaptation where I can have the metadata passed when I call 

`frame_tensor = val2_transforms(frame_tensor)`

This is the whole function:

```
# Define MONAI transforms
val2_transforms = Compose([
    EnsureType(),  # Convert to Tensor
    NormalizeIntensity(nonzero=True, channel_wise=True),  # Normalize each channel
    SpatialPad(method="end", spatial_size=(2048, 2048, 48)),  # Pad to target size
    SpatialCrop(roi_start=(0, 0, 0), roi_end=(2048, 2048, 48))  # Crop (in case padding exceeded)
])

def infer_from_nd2(nd2_path, nd2_chan, model, device="cuda:0", roi_size=None):
    import tifffile
    """
    Load an .nd2 file using bioio-nd2, apply MONAI transforms, and run inference using a MONAI model.
    
    Args:
        nd2_path (str): Path to the .nd2 file.
        nd2_chan (int): Channel index to load.
        model (torch.nn.Module): Pretrained MONAI 3D model.
        device (str): Device to run inference on.
        roi_size (tuple, optional): ROI size for sliding window inference.

    Returns:
        dict: A dictionary with visit points as keys and inferred tensors as values.
    """


    # Load ND2 file
    nd2 = BioImage(nd2_path,reader=bioio_nd2.Reader)
    metadata = nd2.metadata
    # n_visits = metadata.sizes.get('v', 1)  # Number of visit points, default to 1 if not present
    the_z = 15  # Z-slice to visualize
    
    model.to(device)
    model.eval()
    # results = {}

    with torch.no_grad():
        for v in nd2.scenes:
            # Read image data for the visit point and specified channel
            nd2.set_scene(v)
            frame = nd2.get_image_dask_data("XYZ", T=0, C=nd2_chan)  # Shape: (Z, Y, X)
            frame = frame.astype(np.float32)
            frame = frame.compute()

            # Visualize the original frame
            plt.figure("check", (12, 6))
            plt.subplot(1, 2, 1)
            plt.imshow(np.swapaxes(frame,0,2)[the_z], cmap='gray')
            plt.title(f"Original - Visit {v}")
            
            # Convert to torch tensor and add channel dimension
            frame_tensor = torch.tensor(frame).unsqueeze(0)  # Shape: (C, D, H, W)

            # Apply MONAI transforms
            frame_tensor = val2_transforms(frame_tensor)

            # Ensure batch dimension
            frame_tensor = frame_tensor.unsqueeze(0).to(device)  # Shape: (1, C, D, H, W)

            # Run inference
            if roi_size is None:
                output = model(frame_tensor)
            else:
                sw_batch_size = 1
                output = sliding_window_inference(frame_tensor, roi_size, sw_batch_size, model, progress=True)

            # Process output
            output = torch.argmax(output[0], dim=0).detach().cpu()
            # results[v] = output

            # Visualize output
            plt.subplot(1, 2, 2)
            plt.imshow(np.swapaxes(output,0,2)[the_z],
                       # cmap='gray'
                       )
            plt.title(f"Output - Visit {v}")
            plt.show()
            
            # fname_cells = nd2_path.replace(".nd2",f"_s{str(nd2.current_scene_index).zfill(2)}_segres.tif")
            fname_cells = nd2_path.replace(".nd2",f"_s{str(nd2.current_scene_index).zfill(2)}_unet.tif")
            
            print(f"Processed {nd2_path}, Saves {fname_cells}, Visit Point: {v}")
            tifffile.imwrite(fname_cells,
                             np.swapaxes(output,0,2),
                             compression='lzw',
                             metadata={'axes':'ZYX', 'mode':'labels'})
    return True
```

## Comments
### Comment by joaomamede at 2025-03-12T05:33:19Z
This is how I went around with .tiff files
If you just have a 2D tiff it's easy.
please note that the ITK reader only gets the metadata from resolution.
```
def save_tiff(data, filepath, dtype, pixel_size):
    """Save data as a TIFF file (ZYX format) with correct metadata for ITK."""
   _resolution = (1/pixel_size[2], 1/pixel_size[1]),
    metadata = {
        'spacing': pixel_size[0],  # Z spacing
        'spacing_units': ('microns', 'microns', 'microns'),
        'physical_size_x': pixel_size[1],
        'physical_size_y': pixel_size[2],
    }

    tiff.imwrite(filepath, data.astype(dtype), compression="lzw", metadata=metadata, resolution=_resolution)
    
```

I am sure that there's a way to do a MapTransform that can grab the "image_description" from the dataset[0]['key'].meta['image_description'). and reapply it in  dataset[0]['key'].meta['spacing'].

What I end up doing was saving the tiffs as ome.tiff (easier for me as I have many libraries doing it already).
Then using this map transform:

```
class OMEZSpacingFromFileD(MapTransform):
    """
    Extract (Z, Y, X) spacing from OME-TIFF metadata and inject it into `meta['spacing']`.
    """

    def __init__(self, keys, default_z=1.0, default_y=1.0, default_x=1.0):
        """
        Args:
            keys: List of keys to process (e.g., ["image", "label"]).
            default_z: Default Z spacing if not found.
            default_y: Default Y spacing if not found.
            default_x: Default X spacing if not found.
        """
        super().__init__(keys)
        self.default_z = default_z
        self.default_y = default_y
        self.default_x = default_x

    def __call__(self, data: Dict[Hashable, Any]) -> Dict[Hashable, Any]:
        d = dict(data)
        for key in self.keys:
            if key not in d:
                print(f"Warning: key '{key}' not found in data dictionary. Skipping...")
                continue

            file_path = d[key].meta.get('filename_or_obj', None)
            if file_path is None:
                print(f"Warning: no 'filename_or_obj' found in meta for '{key}'. Skipping...")
                continue

            try:
                ome = from_tiff(file_path)
                # Extract physical sizes (check for None)
                image_meta = ome.images[0].pixels
                z_size = image_meta.physical_size_z or self.default_z
                y_size = image_meta.physical_size_y or self.default_y
                x_size = image_meta.physical_size_x or self.default_x

                # Set the spacing in MONAI meta
                d[key].meta["spacing"] = (x_size, y_size, z_size)
                # print(f"[INFO] Set spacing for '{key}': (Z={z_size}, Y={y_size}, X={x_size})")

            except Exception as e:
                # print(f"[ERROR] Failed to read OME metadata from {file_path}: {e}")
                # Fallback to default spacing
                d[key].meta["spacing"] = (self.default_x, self.default_y, self.default_z)
                # print(f"[INFO] Using default spacing for '{key}': (Z={self.default_z}, Y={self.default_y}, X={self.default_x})")

        return d

```


make the transforms with:
```
train_transforms = Compose([
    LoadImaged(keys=["image", "heatmap"],
            #    reader=bla.ITKReader
               ),
    **OMEZSpacingFromFileD(keys=["image", "heatmap"]),**
    EnsureChannelFirstd(keys=["image", "heatmap"]),
    EnsureTyped(keys=["image", "heatmap"]),
    ]),
```

And the spacing metadata is now well populated

```
item = train_ds[0]
item['image'].meta
```

> 
> {'ImageDescription': '<?xml version="1.0" encoding="UTF-8"?><OME xmlns="http://www.openmicroscopy.org/Schemas/OME/2016-06" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.openmicroscopy.org/Schemas/OME/2016-06 http://www.openmicroscopy.org/Schemas/OME/2016-06/ome.xsd" UUID="urn:uuid:aa937b66-fefe-11ef-9a34-a8a1599d9088"  Creator="tifffile.py 2024.2.12"><Image ID="Image:0" Name="Image0"><Pixels ID="Pixels:0" DimensionOrder="XYCZT" Type="uint16" SizeX="128" SizeY="128" SizeC="1" SizeZ="45" SizeT="1" PhysicalSizeX="0.108333333333333" PhysicalSizeY="0.108333333333333" PhysicalSizeZ="0.5"><Channel ID="Channel:0:0" SamplesPerPixel="1"><LightPath/></Channel><TiffData IFD="0" PlaneCount="45"/></Pixels></Image></OME>',
>  'Software': 'tifffile.py',
>  'spacing': (0.108333333333333, 0.108333333333333, 0.5),
>  original_affine: array([[-2.75166669,  0.        ,  0.        ,  0.        ],
>         [ 0.        , -2.75166669,  0.        ,  0.        ],
>         [ 0.        ,  0.        ,  1.        ,  0.        ],
>         [ 0.        ,  0.        ,  0.        ,  1.        ]]),
>  space: RAS,
>  affine: tensor([[   2.7517,    0.0000,    0.0000, -349.4617],
>          [   0.0000,    2.7517,    0.0000, -349.4617],
>          [   0.0000,    0.0000,    1.0000,    0.0000],
>          [   0.0000,    0.0000,    0.0000,    1.0000]], dtype=torch.float64),
>  spatial_shape: array([128, 128,  45]),
>  original_channel_dim: nan,
>  'filename_or_obj': '/processed_images/tiff/Ctlvirus_noVPX_T6h_v007_c03_crop001.tiff'}
> 
> 
> 
>

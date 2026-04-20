# Discussion #8506: Customized labels for 3D datasets
**Repository:** Project-MONAI/MONAI
**Author:** yangjuanyj113
**Created At:** 2025-07-03T02:03:13Z

## Description
Hello! I'm currently using the 3D Retinanet provided by MONAI for the detection of my customized dataset, but I'm confused with a couple of questions regarding the labeling of the dataset and the coordinate system of the images. The organization of my dataset is as follows:1. CBCT images are in the default LPS coordinate system, and all CBCT alignments are performed in 3D Slicer.2. boxMarksup annotations in 3D Slicer software to get ROIs, and the coordinates of the ROIs are exported directly by 3D Slicer as RAS coordinates, which I subsequently converted into CBCT voxel coordinates.3. I input the CBCT image with LPS orientation information as LPS and voxel coordinates as labels into Retinanet for training, and the transforms of my training dataset are as follows: 
train_transforms = Compose( 
 [ 
 LoadImaged(keys=[image _key], image_only=False, meta_key_postfix="meta_dict"), 
 EnsureTyped(keys=[image_key], dtype=torch.float16), 
 ConvertBoxToStandardModed(box_keys=[box_key],  mode=gt_box_mode),
 StandardizeEmptyBoxd( 
            box_keys=[box_key], 
            box_ref_image_keys=image_key, 
 ),

 RandCropBoxByPosNegLabeld( 
     image_keys=[image_key], 
     label_keys=[label_key], 
     box_keys=[box_key], 
     spatial_size=[48, 48, 48], 
     num_samples=4,
     pos=1, 
     neg=1, 
     whole_box=True, 
     allow_smaller=True, 
 ), 
 ClipBoxToImaged( 
     box_keys=[box_key], 
     label_keys=[label_key], 
     box_ref_image_keys=image _key, 
     remove_empty=True, 
 ), 
]) 
Is it ok to use LPS coordinates for custom datasets and voxel coordinates for labels? Or do I need to convert both images and labels to RAS coordinates? I hope you can answer my query in your busy schedule, I will be grateful.

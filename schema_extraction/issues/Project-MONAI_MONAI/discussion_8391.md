# Discussion #8391: Need clarification - new to monai
**Repository:** Project-MONAI/MONAI
**Author:** pure-rgb
**Created At:** 2025-03-17T22:11:52Z

## Description
I have some questions.

In this code example https://github.com/Project-MONAI/tutorials/blob/main/3d_segmentation/brats_segmentation_3d.ipynb

```
train_transform = Compose(
    [
        # load 4 Nifti images and stack them together
        LoadImaged(keys=["image", "label"]),
        EnsureChannelFirstd(keys="image"),
        EnsureTyped(keys=["image", "label"]),
        ConvertToMultiChannelBasedOnBratsClassesd(keys="label"),
        Orientationd(keys=["image", "label"], axcodes="RAS"),
        Spacingd(
            keys=["image", "label"],
            pixdim=(1.0, 1.0, 1.0),
            mode=("bilinear", "nearest"),
        ),
        RandSpatialCropd(keys=["image", "label"], roi_size=[224, 224, 144], random_size=False),
        RandFlipd(keys=["image", "label"], prob=0.5, spatial_axis=0),
        RandFlipd(keys=["image", "label"], prob=0.5, spatial_axis=1),
        RandFlipd(keys=["image", "label"], prob=0.5, spatial_axis=2),
        NormalizeIntensityd(keys="image", nonzero=True, channel_wise=True),
        RandScaleIntensityd(keys="image", factors=0.1, prob=1.0),
        RandShiftIntensityd(keys="image", offsets=0.1, prob=1.0),
    ]
)
val_transform = Compose(
    [
        LoadImaged(keys=["image", "label"]),
        EnsureChannelFirstd(keys="image"),
        EnsureTyped(keys=["image", "label"]),
        ConvertToMultiChannelBasedOnBratsClassesd(keys="label"),
        Orientationd(keys=["image", "label"], axcodes="RAS"),
        Spacingd(
            keys=["image", "label"],
            pixdim=(1.0, 1.0, 1.0),
            mode=("bilinear", "nearest"),
        ),
        NormalizeIntensityd(keys="image", nonzero=True, channel_wise=True),
    ]
)
```

1. what is the role of EnsureTyped(keys=["image", "label"])
2. what does following two layer exactly do and how they affect the training
```python
Orientationd(keys=["image", "label"], axcodes="RAS"),
Spacingd(
     keys=["image", "label"],
     pixdim=(1.0, 1.0, 1.0),
     mode=("bilinear", "nearest"),
)
```
3. what is meta information? I learned that we can turn it off from EnsureTyped by setting track meta to false. By setting it to false, is it wrong, coz my training go kinda disaster. If so important, why not make in immutable for end user?
4. For which transformation meta track are so important? I noticed for operation like orientation, spacing  - it is but for NormalizeIntensityd or Resize - it may not - could be wrong.
5. For some medical data, in a sample (say 3d), there are lots of black / blank slice, no labels > 0. How does monai handles them? Dropping them or what?
6. Take a look at this example https://github.com/Project-MONAI/tutorials/blob/main/3d_segmentation/swin_unetr_btcv_segmentation_3d.ipynb . Here it is used

```
train_transforms = Compose(
    [
        LoadImaged(keys=["image", "label"], ensure_channel_first=True),
        ScaleIntensityRanged(
            keys=["image"],
            a_min=-175,
            a_max=250,
            b_min=0.0,
            b_max=1.0,
            clip=True,
        ),
        CropForegroundd(keys=["image", "label"], source_key="image"),
        Orientationd(keys=["image", "label"], axcodes="RAS"),
        Spacingd(
            keys=["image", "label"],
            pixdim=(1.5, 1.5, 2.0),
            mode=("bilinear", "nearest"),
        ),
        EnsureTyped(keys=["image", "label"], device=device, track_meta=False),
        RandCropByPosNegLabeld(
            keys=["image", "label"],
            label_key="label",
            spatial_size=(96, 96, 96),
            pos=1,
            neg=1,
            num_samples=num_samples,
            image_key="image",
            image_threshold=0,
        ),
        RandFlipd(
            keys=["image", "label"],
            spatial_axis=[0],
            prob=0.10,
        ),
        RandFlipd(
            keys=["image", "label"],
            spatial_axis=[1],
            prob=0.10,
        ),
        RandFlipd(
            keys=["image", "label"],
            spatial_axis=[2],
            prob=0.10,
        ),
        RandRotate90d(
            keys=["image", "label"],
            prob=0.10,
            max_k=3,
        ),
        RandShiftIntensityd(
            keys=["image"],
            offsets=0.10,
            prob=0.50,
        ),
    ]
)
val_transforms = Compose(
    [
        LoadImaged(keys=["image", "label"], ensure_channel_first=True),
        ScaleIntensityRanged(keys=["image"], a_min=-175, a_max=250, b_min=0.0, b_max=1.0, clip=True),
        CropForegroundd(keys=["image", "label"], source_key="image"),
        Orientationd(keys=["image", "label"], axcodes="RAS"),
        Spacingd(
            keys=["image", "label"],
            pixdim=(1.5, 1.5, 2.0),
            mode=("bilinear", "nearest"),
        ),
        EnsureTyped(keys=["image", "label"], device=device, track_meta=True),
    ]
)
```
For training transform, the track meta is set as False in the middle, why not beginning? And in the validation data, it is used and set True at the end, why this difference against traning transform.

These are some of my primary novice questions/concern. Would you please help clarifying?

## Comments
### Comment by cugwu at 2025-03-19T11:30:53Z
1. EnsureTyped(keys=["image", "label"]]): This function ensures that the input data selected by the keys is a PyTorch Tensor or NumPy array; in other words, it converts the data to the proper data type.
2. Orientationd(keys=["image", "label"], axcodes="RAS") changes the image orientation. I don't think it affects the training, so just keep the default one, which is 'RAS'. Regarding Spacingd(), it is a way to re-sample the input image. Depending on the size of the organs or tumours you try to segment, spacing can affect the performance. The re-sample will change the shape of your data, so be sure to add a resize or padding transform after it, if your model expects a particular data resolution.

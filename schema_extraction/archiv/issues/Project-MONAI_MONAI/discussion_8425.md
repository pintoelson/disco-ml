# Discussion #8425: Understanding Task01_BrainTumour Dataset and Image Labels Retrieval
**Repository:** Project-MONAI/MONAI
**Author:** agokli
**Created At:** 2025-04-22T01:09:10Z

## Description
Behind the scene I will like to understand how images and labels are retrieved from nifti files from imagesTr and labelsTr folders.  Various turtorials presents logics: (an example from Weakly Supervised Anomaly Detection with Implicit Guidance)

channel = 0  # 0 = Flair
assert channel in [0, 1, 2, 3], "Choose a valid channel"

train_transforms = transforms.Compose(
    [
        transforms.LoadImaged(keys=["image", "label"]),
        transforms.EnsureChannelFirstd(keys=["image", "label"]),
        transforms.Lambdad(keys=["image"], func=lambda x: x[channel, :, :, :]),
        transforms.EnsureChannelFirstd(channel_dim="no_channel", keys=["image"]),
        transforms.EnsureTyped(keys=["image", "label"]),
        transforms.Orientationd(keys=["image", "label"], axcodes="RAS"),
        transforms.Spacingd(keys=["image", "label"], pixdim=(3.0, 3.0, 2.0), mode=("bilinear", "nearest")),
        transforms.CenterSpatialCropd(keys=["image", "label"], roi_size=(64, 64, 44)),
        transforms.ScaleIntensityRangePercentilesd(keys="image", lower=0, upper=99.5, b_min=0, b_max=1),
        transforms.RandSpatialCropd(keys=["image", "label"], roi_size=(64, 64, 1), random_size=False),
        transforms.Lambdad(keys=["image", "label"], func=lambda x: x.squeeze(-1)),
        transforms.CopyItemsd(keys=["label"], times=1, names=["slice_label"]),
        transforms.Lambdad(keys=["slice_label"], func=lambda x: 2.0 if x.sum() > 0 else 1.0),
    ]
)
train_ds = DecathlonDataset(
    root_dir=root_dir,
    task="Task01_BrainTumour",
    section="training",
    cache_rate=1.0,  # you may need a few Gb of RAM... Set to 0 otherwise
    num_workers=4,
    download=True,  # Set download to True if the dataset hasn't been downloaded yet
    seed=0,
    transform=train_transforms)

train_loader = DataLoader(
    train_ds, batch_size=batch_size, shuffle=True, num_workers=4, drop_last=True, persistent_workers=True
)

while iteration < max_epochs:
    for batch in train_loader:
        iteration += 1
        model.train()
        images, classes = batch["image"].to(device), batch["slice_label"].to(device)
      ..  .    ..    ...
  
**Questions:**

(a) The images and labels in nifti format (imagesTr and labelsTr folders).  Behind scene, how are images and labels are retrieved from those nifiti files?

(b) The statement  transforms.Lambdad(keys=["slice_label"], func=lambda x: 2.0 if x.sum() > 0 else 1.0) retrives slice_label values accordingly (conditionally).  So, what are these sums within underneath logic?

(c) I really want to use other BRATS data , where images and labels are stored as nifit files and then use MONAI transforms.

Can you please provide possible solution(s) or pointer(s) or tutorials?

Thanks

Avinash Gokli

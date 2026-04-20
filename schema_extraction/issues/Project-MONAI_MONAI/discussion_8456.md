# Discussion #8456: Why does inverse transformation fail when using ToTensord in the MONAI pipeline?
**Repository:** Project-MONAI/MONAI
**Author:** emi-dm
**Created At:** 2025-05-19T14:09:19Z

## Description
Hello!

I'm running into an issue when trying to invert a simple MONAI transform pipeline. The inversion works as expected unless I include ToTensord at the end of the pipeline. When ToTensord is present, calling .inverse() on the pipeline raises an error (see below). Is this because ToTensord does not implement an inverse method, or am I missing something about how inversion should work with tensor conversion in MONAI? Any advice on how to properly invert the transforms when using ToTensord would be appreciate

```
import torch
import numpy as np
# Import transforms for dictionaries
from monai.transforms import (
    Compose,
    LoadImaged, # Although we simulate its output, we keep it in the list for reference
    Lambdad,
    RandAffined,
    CropForegroundd,
    DivisiblePadd,
    ToTensord,
    ScaleIntensityd,
    EnsureChannelFirstd # Ensure the channel is first if it isn't already
)
from monai.data import MetaTensor # Fundamental class for inversion

root_dir = "." # Working directory
import os
import nibabel as nib
from glob import glob
from monai.data import create_test_image_3d
from monai.transforms import allow_missing_keys_mode

for i in range(5):
    im, seg = create_test_image_3d(128, 128, 128, num_seg_classes=1, channel_dim=-1)

    n = nib.Nifti1Image(im, np.eye(4))
    nib.save(n, os.path.join(root_dir, f"img{i:d}.nii.gz"))

    n = nib.Nifti1Image(seg, np.eye(4))
    nib.save(n, os.path.join(root_dir, f"seg{i:d}.nii.gz"))

images = sorted(glob(os.path.join(root_dir, "img*.nii.gz")))
segs = sorted(glob(os.path.join(root_dir, "seg*.nii.gz")))
files = [{"img": img, "seg": seg} for img, seg in zip(images, segs)]


# --- Definition of the Transformation Pipeline (Your Pipeline) ---
# We define the transforms pipeline provided by the user.
# We assume that 'keys' in RandAffined refers to ['image', 'label'].
keys = ["img","seg"]

minimal_transforms = Compose(
    [
        LoadImaged(keys, image_only=True),
        ScaleIntensityd("img"),
        CropForegroundd(keys, source_key="img", margin=10),
        ToTensord(keys), # If I remove this, it works
    ]
)

# In a real case, val_transforms would not have random transforms.
# val_transforms = train_transforms # Commented out to avoid confusion in the example

# --- Apply Transformations ---
# We apply the pipeline to the simulated data (which are already MetaTensor).
# MONAI will apply each transform and update the metadata of the MetaTensors
# with the necessary information for the inversion of spatial transforms.
transformed_data = minimal_transforms(files[0]) # We apply to a single file for the example
transformed_image = transformed_data["img"] # Transformed MetaTensor
transformed_label = transformed_data["seg"] # Transformed MetaTensor

print("\n--- After applying Transforms ---")
print("Transformed image data type:", type(transformed_image))
print("Transformed image shape:", transformed_image.shape)
print("Transformed label data type:", type(transformed_label))
print("Transformed label shape:", transformed_label.shape)

# --- Simulate model output ---
# Let's imagine your model takes 'transformed_image' and produces a segmentation.
# The model output MUST have the same spatial shape as 'transformed_image'.
# Let's simulate a binary segmentation output (1 channel) for the image.
# We use torch.rand because model outputs are usually PyTorch tensors.

tran = {"img": transformed_image,}

# --- Invert the Transformation of the Output ---
# Now we invert the simulated model output to map it back to the original space.
# We use the 'transformed_image' MetaTensor to perform the inversion,
# as it contains the history of applied spatial transforms.
# The .inverse() method applies the inverses of the registered spatial transforms
# (DivisiblePadd inverse, CropForegroundd inverse, RandAffined inverse)
# to the 'simulated_model_output'.
# The shape of the inverse output will match the spatial shape of the input
# just before the invertible spatial transforms began (after EnsureChannelFirstd).
# In this case, the inversion maps back to the image space after EnsureChannelFirstd.
# The original spatial shape was (64, 64, 64), EnsureChannelFirstd made it (1, 64, 64, 64).
# Subsequent spatial transforms operated on this.
# The inverse will map back to (1, 64, 64, 64) spatially.
with allow_missing_keys_mode(minimal_transforms):
    inversed_model_output = minimal_transforms.inverse(tran)

print("\n--- After Inverting Model Output ---")
print("Data type of the inverse output:", type(inversed_model_output))
# The expected shape is (1, 64, 64, 64) - channel + original spatial shape
print("Shape of the inverse output:", inversed_model_output["img"].shape)

print("\nProcess completed. The model output and transformed label have been inverted to the original space.")
```

## Comments
### Comment by emi-dm at 2025-05-19T14:45:40Z
I think it is because the inverse of ToTensor's transform is a Numpy Array, so the previous transform (CropForeground) in the compose pipeline expects a "dict" or "MetaTensor" Could it be solved with only removing ToTensor transform from the pipeline?

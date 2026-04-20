# Discussion #8609: `Invertd` warning "transform info of image is not available or no InvertibleTransform applied." in MONAI 1.2.0 (but works in 0.9.0)
**Repository:** Project-MONAI/MONAI
**Author:** dcb937
**Created At:** 2025-10-31T08:53:41Z

## Description
**Description**
When running inference + post-processing with `Invertd` + `SaveImaged` under `monai==1.2.0`, I get the warning:

```
transform info of `image` is not available or no InvertibleTransform applied.
```

and the saved prediction NIfTI results are **not** inverse-transformed back to the original image space (so they are incorrect / misaligned). The same code works as expected under `monai==0.9.0` (the predictions are saved correctly and aligned).

I suspect the `trace_key` is missing during transform in 1.2.0 — but I'm not sure. Below I provide the environment, a minimal reproduction of the pipeline, relevant code excerpts, observed output, and steps-to-reproduce. Any pointers or a fix would be greatly appreciated.

---

## Environment

* MONAI version: `1.2.0` (problem occurs)  **But works with: `monai==0.9.0`**
* PyTorch: 2.4.1
* Python: 3.8.20

---

## Code

```python
import argparse
import os
import numpy as np
import torch

from monai.inferers import sliding_window_inference
from monai.transforms import Compose
from monai.data import decollate_batch

from monai import data, transforms
from monai.data import load_decathlon_datalist


parser = argparse.ArgumentParser(description="Universal segmentation pipeline")
parser.add_argument("--roi_x", default=96, type=int, help="roi size in x direction")
parser.add_argument("--roi_y", default=96, type=int, help="roi size in y direction")
parser.add_argument("--roi_z", default=96, type=int, help="roi size in z direction")
parser.add_argument("--in_channels", default=1, type=int, help="number of input channels")
parser.add_argument("--out_channels", default=3, type=int, help="number of output channels")
args = parser.parse_args()


def denoise_pred(pred_labels: np.ndarray, organ_pseudo: np.ndarray):
    denoised_labels = np.zeros_like(pred_labels)
    
    is_liver = (organ_pseudo == 1)
    denoised_labels[is_liver] = 1
    
    is_tumor_in_pred = (pred_labels == 2)
    
    is_tumor_in_liver = is_tumor_in_pred & is_liver
    denoised_labels[is_tumor_in_liver] = 2

    return denoised_labels


def get_args(data):
    """
    Liver
    """
    if data == "liver":
        data_dir = "../data/Task03_Liver/"
        out_channels = 3
    
    
    infer_overlap = 0.5
    return data_dir, out_channels, infer_overlap

def get_loader(data_dir, js):
    val_transform = transforms.Compose(
        [
            transforms.LoadImaged(keys=["image", "label", "organ_pseudo"]),
            transforms.EnsureChannelFirstd(keys=["image", "label", "organ_pseudo"]),
            transforms.Orientationd(keys=["image", "label", "organ_pseudo"], axcodes="RAS"),
            transforms.Spacingd(
                keys=["image", "label", "organ_pseudo"], pixdim=(1.5, 1.5, 1.5), mode=("bilinear", "nearest", "nearest")
            ),
            transforms.ScaleIntensityRanged(
                keys=["image"], a_min=-175.0, a_max=250.0, b_min=0.0, b_max=1.0, clip=True
            ),
            transforms.CropForegroundd(keys=["image", "label", "organ_pseudo"], source_key="image"),
            transforms.ToTensord(keys=["image", "label", "organ_pseudo"]),
        ]
    )

    val_files = load_decathlon_datalist(os.path.join('.', js), True, "validation", base_dir=data_dir)
    val_ds = data.Dataset(data=val_files, transform=val_transform)
    val_loader = data.DataLoader(
        val_ds,
        batch_size=1,
        shuffle=False,
        num_workers=4,
        sampler=None,
        pin_memory=True,
    )
    return val_loader, val_transform





def inference():
    ckpt_vnet = "snapshots/msd_liver_bs4/fully_supervised_vnet/model_500_0.5080036520957947.pt"
    model_name_vnet = 'load_vnet'

    js = "json/lab.json"
    data_dir, out_channels, infer_overlap = get_args("liver")

    val_loader, val_transform = get_loader(data_dir, js)

    inf_size = (96, 96, 96)

    model_vnet, _ = build_model(model_name_vnet, out_channels, data_dir, ckpt_vnet)
    model_vnet.eval()

    with torch.no_grad():
        for i, batch in enumerate(val_loader):
            val_inputs, val_labels, val_organ_pseudo = (batch["image"].cuda(), batch["label"].cuda(), batch["organ_pseudo"].cuda())
            h, w, d = batch["image_meta_dict"]["spatial_shape"][0]
            img_name = batch["image_meta_dict"]["filename_or_obj"][0].split("/")[-1]
            print(img_name, end=": ")
            print(val_labels.shape)

            val_outputs_vnet = sliding_window_inference(val_inputs, inf_size, 1, model_vnet, overlap=infer_overlap)

            val_outputs_cpu_vnet = val_outputs_vnet.cpu()

            pred_labels_vnet = torch.argmax(val_outputs_cpu_vnet[0], dim=0).numpy()
            
            pred_labels_vnet = denoise_pred(pred_labels_vnet, val_organ_pseudo)

            batch["pred_vnet"] = torch.tensor(pred_labels_vnet).unsqueeze(0).unsqueeze(0)
            print(torch.tensor(pred_labels_vnet).unsqueeze(0).unsqueeze(0).shape)

            post_transforms_vnet = Compose([
                transforms.Invertd(
                    keys=["pred_vnet"], #, 'split_label'
                    transform=val_transform,
                    orig_keys="image",
                    nearest_interp=True,
                    meta_keys="pred_meta_dict",
                    to_tensor=True,
                ),
                transforms.SaveImaged(keys="pred_vnet", 
                        meta_keys="pred_meta_dict" , 
                        output_dir='./pred_vnet', 
                        output_postfix='seg', 
                        resample=False
                ),
            ])
        
            _ = [post_transforms_vnet(i) for i in decollate_batch(batch)]



if __name__ == "__main__":
    inference()
```

---

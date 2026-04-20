# Discussion #8702: Some layers in DiffusionModelUNet are detached and zeroed
**Repository:** Project-MONAI/MONAI
**Author:** AbrightWay
**Created At:** 2026-01-15T14:23:35Z

## Description
Hi folks,

I am encountering the output of Unet model from DiffusionModelUNet being a zero tensor no matter what input I feed into it. Therefore, I look into the source code of the model and found that the convolution of the final layer of the residual block of UNet is a zero module (https://github.com/Project-MONAI/MONAI/blob/57fdd594ac905ab2ea778aa4bb79ccd9a0a03b22/monai/networks/nets/diffusion_model_unet.py#L393)
Also, the output convolution of UNet itself is a zero module too (https://github.com/Project-MONAI/MONAI/blob/57fdd594ac905ab2ea778aa4bb79ccd9a0a03b22/monai/networks/nets/diffusion_model_unet.py#L1720).

Could you please explain why zeroing out these layers, which makes the overal UNet output to be zero. This is quite counterintuitive to me.

Thank you in advanced!

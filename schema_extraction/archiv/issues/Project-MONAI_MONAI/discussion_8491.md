# Discussion #8491: Patch resolution of UNETR
**Repository:** Project-MONAI/MONAI
**Author:** riku-ops
**Created At:** 2025-06-19T07:22:05Z

## Description
By default, the patch resolution is defined as 16×16×16. Due to GPU memory limitations, if we change it to 32×32×32, how should the model architecture be modified?

## Comments
### Comment by id-b3 at 2025-08-19T09:26:36Z
Hi, the patch size for the UNETR is hard-coded to 16 due to the need for modifying the upsampling blocks if the patch size is different.
This has been covered in a previous discussion, in essense you will need to change the patch size in the model and then add an `nn.Upsample` block to the model.

https://github.com/Project-MONAI/MONAI/discussions/4461

# Discussion #8390: How to change model size for latent diffusion
**Repository:** Project-MONAI/MONAI
**Author:** karllandheer
**Created At:** 2025-03-17T17:48:04Z

## Description
I am trying to modify the tutorial shown here: 
https://github.com/Project-MONAI/GenerativeModels/blob/main/tutorials/generative/2d_diffusion_autoencoder/2d_diffusion_autoencoder_tutorial.ipynb

to accomodate my data which is larger in size. For example, my images are 12 channels with an image size of 256x256. Even with a batch size of 1 this gives OOM for GPUs with 16GB RAM. Does anyone know how to address this? One way is to do random cropping transforms, however this then makes inference a bit more confusing. Alternatively I could reduce the model size of Diffusion_AE, however I'm not 100% sure how to do that. Any ideas?

## Comments
### Comment by virginiafdez at 2025-09-05T06:42:47Z
Diffusion models are quite computing-demanding, so it might be possible not to run 2D training on 256x256 images depending on your GPU. However, these are some things you can do to try to reduce memory:

- Use flash attention (this can make attention layers more efficient)
- Remove attention layers (attention, especially at high levels, is quite computing-intensive, setting the attention levels to False will save you some memory)
- Use less number of channels or reduce the number of residual blocks per level

Besides this, as you mention, apply center-crop transforms to try to reduce as much as possible the size of your inputs will help.

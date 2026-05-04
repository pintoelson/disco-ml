# Discussion #8567: Convolution block settings
**Repository:** Project-MONAI/MONAI
**Author:** n-faro
**Created At:** 2025-09-11T13:58:43Z

## Description
I'm kind of confused about the best way to implement a Convolution block. I'm working with 3D medical images (so spatial_dims=3) and have specified dropout_dim=3, but not set norm_dim. Additionally, I set adn_ordering="AND" (activation → normalization → dropout). However, in my training, I'm observing the performance is worse / training is unstable. Thank you for any suggestions!

## Comments
### Comment by NabJa at 2025-09-11T14:12:41Z
Hi, 

setting `spatial_dims=3` is correct in this case. `dropout_dim` and `norm_dim` depend on your architecture. I would advice starting with copying prominent architectures like the  [`ResNet`](https://github.com/Project-MONAI/MONAI/blob/1.5.0/monai/networks/nets/resnet.py#L187-L364) for classification/regression and the [`UNet`](https://github.com/Project-MONAI/MONAI/blob/1.5.0/monai/networks/nets/unet.py#L27-L298) for segmentation tasks.

Unstable training can have many reasons. Make sure to start with a small simple network and gradually make it more complex. [A Recipe for Training Neural Networks](https://karpathy.github.io/2019/04/25/recipe/) by Andrej Karpathy is probably the best starting point I know. Good look! :)

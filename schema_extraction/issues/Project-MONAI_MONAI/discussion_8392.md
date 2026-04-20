# Discussion #8392: MONAI Implementation of Slice-Shift-UNet (SSH-UNet) Check our official code!!!!
**Repository:** Project-MONAI/MONAI
**Author:** cugwu
**Created At:** 2025-03-18T09:28:17Z

## Description
The **ssh-unet** repository (https://github.com/cugwu/ssh-unet) builds on insights from video action recognition to propose **Slice Shift UNet (SSH-UNet)**, a 2D-based model that encodes **3D features with the efficiency of 2D CNNs**. 
It achieves this by applying 2D convolutions (conv-1x3x3) across three orthogonal planes while using **weight sharing** 
to integrate multi-view features. The neglected third dimension is **reintroduced via feature map shifting** along the slice axis.

SSH-UNet is a ri-adaptation of MONAI's **DynUNet**, with most of the code based on the official MONAI implementation.

**With only 6.48M parameters SSH-UNet surpasses famous methods like SwinUNETR and UNETR, which have 86.32M and 79.43M parameters, respectively, on BTCV and AMOS segmentation datasets when used under the same training conditions.**

## Comments
### Comment by pure-rgb at 2025-03-18T23:42:28Z
Thanks for sharing. You seem like working on medical image data. I'm kinda new, could you please answer some of my preliminary quries over here https://github.com/Project-MONAI/MONAI/discussions/8391 TIA.

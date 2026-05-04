# Discussion #8490: Do we need to normalize according to the pretrained model?
**Repository:** Project-MONAI/MONAI
**Author:** rotemorad
**Created At:** 2025-06-18T11:23:13Z

## Description
Hi, I'm using Resnet for classification of MRI and when looking at the tutorials I didn't see normalization as part of the transforms. 

Im using MONAIs ResNet, loading pretrained weights from ImageNet. 
Pytorch specifically states that "The images have to be loaded in to a range of [0, 1] and then normalized using mean = [0.485, 0.456, 0.406] and std = [0.229, 0.224, 0.225]." 

Should I add the normalization or MONAI already handles it?

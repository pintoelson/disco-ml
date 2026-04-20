# Discussion #8434: Multimodality generation?
**Repository:** Project-MONAI/MONAI
**Author:** EnriqueFV
**Created At:** 2025-05-02T09:32:36Z

## Description
Hi,

I need to enhance the size of our dataset, and we have considered using synthetic images. Our dataset is mainly composed of CT, PET, and some MRI and US, and is quite low (20 to 30 studies). For now, the most important modalities for our hypothesis are CT and PET. Given that MAISI can generate new CT images with a high consistency, I considered the possibility that it could generate a multimodal output, considering that we need the correlation between CT and PET signals. As I read over the tutorial, it is trained on several datasets, but one of them they mention for the performance is [autoPET 2023](https://www.nature.com/articles/s41597-022-01718-3), that when I read more into it is compose of both CT and PET modalities. 

So, is it possible to calibrate the model with both modalities in order to let it generate outputs that are consistent between both of them?

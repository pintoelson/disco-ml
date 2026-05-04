# Discussion #8431: ITKReader memory usage
**Repository:** Project-MONAI/MONAI
**Author:** Jorissss
**Created At:** 2025-04-29T06:41:48Z

## Description
When training a model from .mha files using the ITKReader ImageReader class, memory usage is very high and unstable. This happens to a much lesser extent after converting files to nifti format and using the NiBabelReader ImageReader. We could also reduce the problem by adding an explicit gc.collect statement after each iteration. Still, we see that the 'ramp up' of memory usage using the ITKReader is much faster than for the NiBabelReader.

Any ideas on what causes this behaviour and the best way to handle it? We would prefer to use .mha files for training as that is the default format we use to handle image data.

Below are some plots of memory use, measured through `docker stats`. Each run was done in a separate container. First image is the default ITKReader with .mha images. Second is the NiBabelReader on nifti images. Third is the ITKReader with explicit gc.collect calls. Note that in the first image the run crashes at around ~60 epochs due to going over the container's memory limit. The other 2 images/runs ran the full 150 epochs and then stopped.

![image](https://github.com/user-attachments/assets/e93c0565-e945-4196-b834-0551b8f34e1e)

![image](https://github.com/user-attachments/assets/b56a7859-8334-458a-b40f-89c2cc77885b)

![image](https://github.com/user-attachments/assets/2180af97-980a-45e9-a489-e7948c94627c)

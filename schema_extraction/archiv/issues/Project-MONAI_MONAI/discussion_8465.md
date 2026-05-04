# Discussion #8465: How to accelerate inference for lung nodule detection
**Repository:** Project-MONAI/MONAI
**Author:** zhuofalinHJh
**Created At:** 2025-05-30T06:49:35Z

## Description
**How to accelerate inference for lung nodule detection**
-----------------
1. I used the code of [this project](https://github.com/Project-MONAI/tutorials/tree/main/detection) to complete the training of the lung nodule detection model. Now I plan to convert it to an onnx model for inference acceleration, but I don’t know how to do it?
2. How can I accelerate the inference of lung nodule detection when the hardware remains unchanged?
-----------------
**My development environment**

1. Windows 11 pro
2. nvidia info
```shell
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 576.52                 Driver Version: 576.52         CUDA Version: 12.9     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                  Driver-Model | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 4070 ...  WDDM  |   00000000:01:00.0  On |                  N/A |
| N/A   46C    P8              2W /  140W |     629MiB /   8188MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
```
3. monai: 1.4.0

## Comments
### Comment by zhuofalinHJh at 2025-05-30T06:57:37Z
@ericspod @tvercaut, can you help me? thanks

### Comment by zhuofalinHJh at 2025-06-11T06:56:11Z
Thank you for your reply. After actual testing, I found that the detection effect of 3D RetinaNet is not very good. Now I plan to revise the lung nodule detection method.

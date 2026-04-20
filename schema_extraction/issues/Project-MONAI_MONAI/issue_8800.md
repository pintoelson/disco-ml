# Issue #8800: Potentially wrong device using_cuda variable status in monai/auto3dseg/analyzer.py
**Repository:** Project-MONAI/MONAI
**Author:** benediktjohannes
**Status:** closed
**Created At:** 2026-04-02T13:23:03Z

## Description
We set the label_tensor device to the device of the image_tensor here, but we already determined whether cuda is set or not (using_cuda) above by checking whether any of both tensors uses cuda. So in case we got label_tensor to use cuda and image_tensor not, then we would first set using_cuda to True, but then we check whether if label_tensor.device is != image_tensor.device which is True and therefore we set the device of label_tensor to non-cuda (e.g. cpu) which means that now both tensors use cpu while using_cuda is still wrongly set to True.

(see the detailed explaination in #8708, I just opened this issue here so that we don't forget about this since #8708 is already merged, but still got this potential issue open)

## Comments
### Comment by garciadias at 2026-04-02T14:41:58Z
I will create the PR now.
### Comment by benediktjohannes at 2026-04-02T15:16:52Z
Thank you for doing this!

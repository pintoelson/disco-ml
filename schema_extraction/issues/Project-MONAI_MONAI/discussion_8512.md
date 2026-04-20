# Discussion #8512: TorchIO import fail
**Repository:** Project-MONAI/MONAI
**Author:** chiaraalbi46
**Created At:** 2025-07-18T08:42:07Z

## Description
I'm trying to use TorchIO wrapper for including some torchio augmentations in MONAI training, but I can not import the TorchIO class from monai.transforms. I'm using Python 3.8 and monai 1.3.2. 
Can you help me ? 
Thank you in advice

## Comments
### Comment by NabJa at 2025-08-04T20:27:38Z
TorchIO requires `python >= 3.9`. Try upgrading you python and `pip install torchio`. That should fix it.

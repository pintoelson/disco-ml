# Discussion #8662: UserWarning: Using a non-tuple sequence for multidimensional indexing is deprecated.
**Repository:** Project-MONAI/MONAI
**Author:** jizhang02
**Created At:** 2025-12-16T15:18:04Z

## Description
Hello,

As title shows, when I training the model, there is a warning:

```
C:\Users\Jing\miniconda3\Lib\site-packages\monai\inferers\utils.py:370: 
UserWarning: 
Using a non-tuple sequence for multidimensional indexing is deprecated and will be changed in pytorch 2.9;
use x[tuple(seq)] instead of x[seq]. 
In pytorch 2.9 this will be interpreted as tensor index, 
x[torch.tensor(seq)], which will result either in an error or a different result (Triggered internally at
C:\actions-runner\_work\pytorch\pytorch\pytorch\torch\csrc\autograd\python_variable_indexing.cpp:351.)
```

I use `torch 2.9.1 + monai 1.5.1`.
Does anyone know how to solve this warning?
Thank you in advance!
Jing

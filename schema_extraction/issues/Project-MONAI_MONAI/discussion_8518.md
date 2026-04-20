# Discussion #8518: Confusing behaviour for AsDiscrete transform
**Repository:** Project-MONAI/MONAI
**Author:** thibaultdvx
**Created At:** 2025-07-24T15:57:37Z

## Description
There is something confusing with the transform ``AsDiscrete``. In the following example, I have a batch of two predicted probabilities ``[0.3, 0.9]``; so with a threshold set to ``0.5``, the elements of the batch should be mapped to the class ``0`` and ``1`` respectively. This is what I expected to obtain with ``AsDiscrete``:

``` python
from monai.transforms import AsDiscrete, Compose
import torch

predictions = torch.tensor([0.3, 0.9])

# the goal is to obtain torch.tensor([[1., 0], [0., 1.]])

as_discrete = AsDiscrete(to_onehot=2, threshold=0.5, dim=1)
```

But I get: 

``` python
>>> as_discrete(predictions)
metatensor([[1., 0.], [1., 0.]])
```

This fixes the issue:

``` python
as_discrete = Compose([AsDiscrete(threshold=0.5), AsDiscrete(to_onehot=2, dim=1)])
```

``` python
>>> as_discrete(predictions)
metatensor([[1., 0.], [0., 1.]])
```

But still, I find this behaviour very confusing. Does someone have an explanation to justify it?

PS: I'm using **MONAI 1.5.0**

## Comments
### Comment by NabJa at 2025-08-05T07:53:14Z
The current implementation of `AsDiscrete` first applies one-hot encoding and then performs thresholding ([source code](https://github.com/Project-MONAI/MONAI/blob/1.5.0/monai/transforms/post/array.py#L218-L228)). However, one-hot encoding assumes that the input already consists of discrete class indices, e.g., `[0, 1, 2] -> [[1, 0, 0], [0, 1, 0], [0, 0, 1]]`.

This can be a bit counterintuitive when using `AsDiscrete` as a post-processing step for model outputs, especially when the output is probabilistic (e.g., softmax or sigmoid values). In such cases, applying one-hot encoding before thresholding may not be the expected behavior.

Conceptually, it might be clearer to think of `AsDiscrete` as a wrapper that can only perform one transformation at a time. Not really a justification but hopefully an explanation. :D

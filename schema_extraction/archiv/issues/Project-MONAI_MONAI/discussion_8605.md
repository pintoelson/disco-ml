# Discussion #8605: DiceMetric: `mean_batch` and `mean_channel` reduction modes appear to be swapped
**Repository:** Project-MONAI/MONAI
**Author:** gauthamk02
**Created At:** 2025-10-25T14:55:54Z

## Description
**Describe the bug**
The `mean_batch` and `mean_channel` reduction modes in `DiceMetric.aggregate()` appear to be swapped. `mean_batch` returns one value per channel (instead of per batch), and `mean_channel` returns one value per batch (instead of per channel).

 Is this the intended behavior, or am I misunderstanding how data should be accumulated or passed to DiceMetric? In the below example, the dimension of the data is BCHW.

**To Reproduce**
Run:
```python
import torch
from monai.metrics import DiceMetric

n_batches = 3
batch_size, n_classes, h, w = 4, 5, 128, 128

y_pred_batches = [torch.rand(batch_size, n_classes, h, w) for _ in range(n_batches)]
y_batches = [torch.rand(batch_size, n_classes, h, w) for _ in range(n_batches)]

dm = DiceMetric()

for i in range(n_batches):
    dm(y_pred_batches[i], y_batches[i])

# Internal buffer has shape [12, 5] (12 samples total, 5 channels)
print(f"Buffer shape: {dm.get_buffer().shape}")  # [12, 5]

# mean_batch returns 5 values (one per channel, not per batch)
print(f"mean_batch: {dm.aggregate(reduction='mean_batch').shape}")  # [5]

# mean_channel returns 12 values (one per batch, not per channel)  
print(f"mean_channel: {dm.aggregate(reduction='mean_channel').shape}")  # [12]
```

**Expected behavior**
mean_batch should average across channels and return one value per batch: shape [3]
mean_channel should average across batches and return one value per channel: shape [5]


**Environment**

Ensuring you use the relevant python executable, please paste the output of:

```
MONAI version: 1.5.0
Numpy version: 2.2.6
Pytorch version: 2.6.0+cu124
```

**Additional context**
The problem appears to be in `monai/metrics/utils.py:do_metric_reduction()` lines 113-121. I am not sure if the bug affects other metrics using this function too.

## Comments
### Comment by KumoLiu at 2025-10-28T02:37:21Z
Hi @gauthamk02, thanks for reporting this.
In this repo, we have defined `MEAN_BATCH` to calculate the average across the batch dimension, and `MEAN_CHANNEL` to calculate the average across the channel dimension.
https://github.com/Project-MONAI/MONAI/blob/69f3dd26ed2a65e89ae89d951bb16f2dcb4d7c5d/monai/metrics/utils.py#L113

https://github.com/Project-MONAI/MONAI/blob/69f3dd26ed2a65e89ae89d951bb16f2dcb4d7c5d/monai/metrics/utils.py#L119

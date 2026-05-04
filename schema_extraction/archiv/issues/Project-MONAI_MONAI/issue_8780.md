# Issue #8780: Bug in `make_gaussian_kernel` causes incorrect `LocalNormalizedCrossCorrelationLoss` when `kernel_size > 3`
**Repository:** Project-MONAI/MONAI
**Author:** xiyizhou16
**Status:** closed
**Created At:** 2026-03-18T07:36:25Z

## Description
**Describe the bug**
I encountered a severe numerical issue when using `LocalNormalizedCrossCorrelationLoss` with `kernel_type="gaussian", kernel_size=15`. When calculating the LNCC of two completely identical images, the loss does not converge to `-1.0` (or `1.0` for metric). Instead, it outputs a surprisingly small value (e.g., around `0.08`).

After diving into the source code, I found that the bug originates from `make_gaussian_kernel()`, specifically how the `truncated` parameter is passed to `gaussian_1d()`.

**To Reproduce**
Here is a minimal reproducible example. Calculating the LNCC of two identical tensors should yield a loss close to `-1.0`.

```python
import torch
from monai.losses import LocalNormalizedCrossCorrelationLoss

# Create two identical dummy tensors
target = torch.rand(1, 1, 64, 64, 64)
pred = target.clone()

# Calculate LNCC with a Gaussian window
lncc_metric = LocalNormalizedCrossCorrelationLoss(
    spatial_dims=3, 
    kernel_size=15, 
    kernel_type="gaussian", 
    reduction="mean"
)

loss = lncc_metric(pred, target)

print(f"Calculated Loss (Expected ~ -1.0): {loss.item()}")
print(f"Generated Kernel Max Value: {lncc_metric.kernel.max().item()}")
```

**Output:**
```text
Calculated Loss (Expected ~ -1.0): -1.2499695695817811e-14
Generated Kernel Max Value: 0.00014774840383324772
```

**Environment**
```text
Python version: 3.11.13
MONAI version: 1.5.2
Numpy version: 2.3.4
Pytorch version: 2.8.0+cu126
MONAI flags: HAS_EXT = False, USE_COMPILED = False, USE_META_DICT = False
MONAI rev id: d18565fb3e4fd8c556707f91ac280a2dc3f681c1
```

### Root Cause Analysis:
In `monai/losses/image_dissimilarity.py`, the `make_gaussian_kernel` function is implemented as follows:
```python
def make_gaussian_kernel(kernel_size: int) -> torch.Tensor:
    sigma = torch.tensor(kernel_size / 3.0)
    kernel = gaussian_1d(sigma=sigma, truncated=kernel_size // 2, approx="sampled", normalize=False) * (2.5066282 * sigma)
    return kernel[:kernel_size]
```

According to the implementation of `gaussian_1d`, the `truncated` parameter dictates the truncation bound in units of **standard deviations** (i.e., `radius = truncated * sigma`).
However, `make_gaussian_kernel` incorrectly passes the absolute pixel radius (`kernel_size // 2`) to `truncated`.

For example, if `kernel_size=15`:
1. `sigma = 5.0`
2. `truncated = 7`
3. `gaussian_1d` interprets the radius as $7 \times 5.0 = 35$ pixels. It generates an array of length 71 (from `x = -35` to `+35`), where the actual peak is at index 35.
4. Finally, `kernel[:kernel_size]` slices only the first 15 elements (the extreme left tail, from `x = -35` to `x = -21`). 

This results in a 1D kernel filled with extremely tiny values (e.g., $10^{-4}$ to $10^{-11}$). When expanded to 3D, the kernel values become so astronomically small (around $10^{-12}$) that the local variance falls far below the `smooth_dr` threshold (`1e-5`). Consequently, `smooth_dr` dominates the denominator, corrupting the LNCC calculation entirely.

## Comments
### Comment by atharvajoshi01 at 2026-04-08T01:55:26Z
Clear bug. The truncated parameter is being set to kernel_size // 2 but gaussian_1d expects it as the number of standard deviations. With kernel_size=15 this means truncated=7, so the Gaussian gets truncated at 7 sigma and the kernel values become negligibly small. I'll send a fix.

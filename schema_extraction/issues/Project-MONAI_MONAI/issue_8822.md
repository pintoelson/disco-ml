# Issue #8822: [Bug] `SSIMLoss` docstring examples are incorrect: `1-SSIMLoss()(x,y)` negates the loss
**Repository:** Project-MONAI/MONAI
**Author:** Zeesejo
**Status:** open
**Created At:** 2026-04-11T18:28:45Z

## Description
## Bug Description

The docstring examples in `SSIMLoss.forward()` (file: `monai/losses/ssim_loss.py`, ~line 100) all show:

```python
print(1-SSIMLoss(spatial_dims=2)(x,y))
```

However, `SSIMLoss.forward()` already computes `1 - ssim_value` internally (line ~107):
```python
loss: torch.Tensor = 1 - ssim_value
```

So calling `1-SSIMLoss()(x,y)` produces `1 - (1 - ssim) = ssim`, which is the **structural similarity value** — not the loss. This confuses users into thinking they need to subtract from 1 again, leading to incorrect training.

## Expected Behavior

The docstring examples should read:
```python
print(SSIMLoss(spatial_dims=2)(x,y))
```

## Impact

Users following these examples would compute a "loss" that actually **increases** when images become less similar, which is the **opposite** of what is intended. Any training loop based on these examples would train in the wrong direction.

## Location

`monai/losses/ssim_loss.py`, `SSIMLoss.forward` docstring examples (lines 93-113 approx)

## Proposed Fix

Remove the `1-` prefix from each of the three docstring example `print()` statements:

```python
# 2D data
print(SSIMLoss(spatial_dims=2)(x,y))  # was: print(1-SSIMLoss(spatial_dims=2)(x,y))

# pseudo-3D data
print(SSIMLoss(spatial_dims=2)(x,y))  # was: print(1-SSIMLoss(spatial_dims=2)(x,y))

# 3D data
print(SSIMLoss(spatial_dims=3)(x,y))  # was: print(1-SSIMLoss(spatial_dims=3)(x,y))
```

## Chain Context

This issue was found as part of a systematic audit of `monai/losses/` for correctness:
- PR #8818: `image_dissimilarity.py` — `register_buffer` fix for `require_grads`
- Issue #8819: systematic `register_buffer` audit
- Issue #8820 / PR #8821: `spectral_loss.py` — `JukeboxLoss` variable swap fix
- **This issue**: `ssim_loss.py` — docstring example bug

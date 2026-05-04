# Issue #8819: [Bug] `LocalNormalizedCrossCorrelationLoss`: kernel not registered as buffer — silent gradient tracking + wrong device placement
**Repository:** Project-MONAI/MONAI
**Author:** Zeesejo
**Status:** open
**Created At:** 2026-04-11T17:51:56Z

## Description
## Describe the bug

In `monai/losses/image_dissimilarity.py`, `LocalNormalizedCrossCorrelationLoss.__init__` contains two related problems in kernel initialization:

### Problem 1: Typo in `require_grads` (silent no-op)

```python
self.kernel = _kernel(self.kernel_size)
self.kernel.require_grads = False  # BUG: 'require_grads' is NOT a valid tensor attribute!
self.kernel_vol = self.get_kernel_vol()
```

`require_grads` (plural, with trailing `s`) is **not** a valid PyTorch tensor attribute. The correct attribute is `requires_grad`. This line silently does nothing — it creates a new Python attribute called `require_grads` on the tensor object instead of controlling gradient tracking. As a result, **the kernel tensor silently tracks gradients** in every forward pass, consuming unnecessary memory in the computation graph.

### Problem 2: Plain attribute assignment instead of `register_buffer`

Using `self.kernel = ...` (plain attribute) instead of `self.register_buffer("kernel", ...)` means:
- When the user calls `loss.to("cuda")`, `loss.cuda()`, or `loss.half()` on the loss module, **the kernel does NOT move to the target device** — it stays on CPU. This causes a device mismatch at runtime.
- The kernel is **not included** in `state_dict()` / `load_state_dict()` which leads to silent inconsistencies if checkpointing the loss object.

## To Reproduce

```python
import torch
from monai.losses import LocalNormalizedCrossCorrelationLoss

loss = LocalNormalizedCrossCorrelationLoss(spatial_dims=3, kernel_type="gaussian")

# Bug 1: require_grads typo silently does nothing
print(loss.kernel.requires_grad)   # True! Not False as intended
print(hasattr(loss.kernel, 'require_grads'))  # True -- spurious attribute created

# Bug 2: kernel not a registered buffer
print(dict(loss.named_buffers()))  # {} -- kernel is NOT here!
loss.cuda()
print(loss.kernel.device)  # cpu -- kernel did NOT move to GPU!
```

## Expected behavior

- `loss.kernel.requires_grad` should be `False`
- `loss.kernel` and `loss.kernel_vol` should appear in `loss.named_buffers()`
- After `loss.cuda()`, `loss.kernel.device` should be `cuda:0`

## Fix

Replace both assignments with `register_buffer`:

```python
self.register_buffer("kernel", _kernel(self.kernel_size))
self.register_buffer("kernel_vol", self.get_kernel_vol())
```

This is tracked in PR #8818.

## Environment

Affects all versions. Reproducible on MONAI `dev` branch as of 2026-04-11.

## Related chain of issues

This bug reveals a broader pattern worth auditing across the MONAI losses module:
1. `GlobalMutualInformationLoss` — check if `bin_centers` is properly registered as a buffer
2. Other custom loss classes that use constant tensors initialized in `__init__`
3. Test coverage for device movement of loss modules (`loss.cuda()` should not cause device mismatch)

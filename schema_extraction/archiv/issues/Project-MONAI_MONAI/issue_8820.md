# Issue #8820: [Bug] `JukeboxLoss.forward`: `input_amplitude` and `target_amplitude` variable names are swapped
**Repository:** Project-MONAI/MONAI
**Author:** Zeesejo
**Status:** closed
**Created At:** 2026-04-11T18:08:21Z

## Description
## Describe the bug

In `monai/losses/spectral_loss.py`, `JukeboxLoss.forward()` has the variable names `input_amplitude` and `target_amplitude` **swapped**:

```python
def forward(self, input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    input_amplitude = self._get_fft_amplitude(target)   # ← BUG: should be _get_fft_amplitude(input)
    target_amplitude = self._get_fft_amplitude(input)   # ← BUG: should be _get_fft_amplitude(target)

    loss = F.mse_loss(target_amplitude, input_amplitude, reduction="none")
```

## Impact

While this does **not** affect the numerical output of the loss (since MSE is symmetric: `mse(a, b) == mse(b, a)`), the naming is **semantically inverted** which:

1. Makes the code **misleading and confusing** to anyone reading, extending, or debugging it
2. Creates a **silent maintenance hazard** — if anyone adds asymmetric processing (e.g. normalization, weighting, gradient masking) based on input vs. target, the swap will cause subtle, hard-to-debug training errors
3. Violates the principle of least surprise for the standard `forward(input, target)` contract that all PyTorch loss functions follow

## Root Cause

In `forward(self, input, target)`:
- `input_amplitude` is computed from `target` (wrong)
- `target_amplitude` is computed from `input` (wrong)

## Expected behavior

```python
def forward(self, input: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
    input_amplitude = self._get_fft_amplitude(input)    # correct
    target_amplitude = self._get_fft_amplitude(target)  # correct
    loss = F.mse_loss(target_amplitude, input_amplitude, reduction="none")
```

## Location

`monai/losses/spectral_loss.py` lines 55-56

Affects all MONAI versions containing `JukeboxLoss`. Reproducible on `dev` branch as of 2026-04-11.

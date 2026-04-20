# Issue #8775: [BUG] compute_shape_offset triggers PyTorch ≥2.9 breaking change for non-tuple sequence indexing
**Repository:** Project-MONAI/MONAI
**Author:** AryanMoradi
**Status:** closed
**Created At:** 2026-03-17T00:38:39Z

## Description
## Describe the bug
`compute_shape_offset` in `monai/data/utils.py` (line 883) passes `spatial_shape` directly to `np.array()`. When `spatial_shape` is a PyTorch tensor, this triggers the non-tuple sequence multidimensional indexing deprecation that became a breaking change in PyTorch 2.9+.

## To reproduce
Run any pipeline that goes through `SaveImaged` → `NiftiWriter.set_metadata` → `resample_if_needed` → `spatial_resample` → `compute_shape_offset` with PyTorch ≥ 2.9.

## Expected behavior
No error. `spatial_shape` should be converted to a plain Python tuple before being passed to `np.array`.

## Actual behavior
On PyTorch ≥ 2.9, this either raises an error or produces silently wrong results.
On PyTorch 2.8 it was a deprecation warning.

## Environment
- MONAI: 1.5.2
- PyTorch: 2.10.0+cu129
- Python: 3.11
- OS: Windows 11

## Suggested fix
```python
# monai/data/utils.py, line 883
# Before:
shape = np.array(spatial_shape, copy=True, dtype=float)
# After:
shape = np.array(tuple(spatial_shape), copy=True, dtype=float)

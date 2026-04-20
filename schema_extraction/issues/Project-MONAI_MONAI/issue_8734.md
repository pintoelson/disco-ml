# Issue #8734: Feature Request: Support ignore_index / ignore_class in Losses and Metrics
**Repository:** Project-MONAI/MONAI
**Author:** jermmy19998
**Status:** open
**Created At:** 2026-02-07T01:45:03Z

## Description
In practical medical image segmentation, it is very common to have label values that should be ignored (e.g. padding, unlabeled regions, auxiliary classes).

Currently, MONAI losses and metrics (e.g. DiceLoss, DiceMetric, MeanIoU) do not natively support ignoring specific classes or label values. Users must manually mask predictions and targets, which is error-prone and inconsistent.

Request:
Add native support for an argument such as ignore_index or ignore_classes to losses and metrics.

Example:

`DiceCELoss(include_background=False, ignore_index=2)`
`DiceMetric(include_background=False, ignore_index=2)`


Expected behavior:

Voxels with ignored labels are excluded from numerator and denominator

Works consistently for binary and multi-class segmentation

Compatible with reduction="mean" and get_not_nans

This would improve correctness, reproducibility, and align MONAI with common PyTorch APIs (e.g. CrossEntropyLoss(ignore_index)).

Thanks for considering!

## Comments
### Comment by Rusheel86 at 2026-02-14T09:01:48Z
This seems like an interesting and valuable feature for medical imaging so I'd like to help implement ignore_index by introducing a binary masking step that excludes specified label values from the calculations.
### Comment by jermmy19998 at 2026-02-15T02:20:57Z
could merge with Ignore Class #8667

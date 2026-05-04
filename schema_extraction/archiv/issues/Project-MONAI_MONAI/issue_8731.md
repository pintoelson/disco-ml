# Issue #8731: Feature Request: Add SparseDice, SparseClDice, CenterlineDice Losses and 3D TransUNet
**Repository:** Project-MONAI/MONAI
**Author:** jermmy19998
**Status:** open
**Created At:** 2026-02-04T08:48:46Z

## Description
Hello MONAI team,

I would like to request the addition of several features to MONAI that could benefit the community for 3D medical image segmentation tasks:

SparseDiceLoss – A Dice loss variant that supports sparse labels, useful for multi-class segmentation with incomplete annotations.

SparseClDiceLoss (Centerline Dice for sparse data) – Combines clDice and sparse label support for tubular structures such as vessels, fibers, or centerlines.

CenterlineDiceLoss (clDiceLoss) – Measures topological agreement between predicted and ground-truth structures by comparing their soft skeletons; very useful for thin elongated objects in 2D/3D.

3D TransUNet – Extend the current 2D TransUNet to full 3D, to handle volumetric medical images directly.

These additions would greatly help users working on complex 3D segmentation tasks, especially with sparse annotations and tubular structures.

Thank you for considering this feature request!

## Comments
### Comment by Asmodasis at 2026-03-04T23:03:43Z
I'd be willing to attempt these features if no one has been assigned to it yet.

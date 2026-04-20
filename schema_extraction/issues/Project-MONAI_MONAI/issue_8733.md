# Issue #8733: Feature Request: Evaluation of Semantic Segmentation Metrics on a per-component basis
**Repository:** Project-MONAI/MONAI
**Author:** alexanderjaus
**Status:** open
**Created At:** 2026-02-06T15:12:41Z

## Description
**Is your feature request related to a problem? Please describe.**

Current MONAI segmentation metrics aggregate scores globally. In multi-instance medical segmentation tasks this can mask clinically relevant failure modes, e.g. missing small lesions while achieving high Dice scores due to dominant large structures. There is no native support for connected component aware evaluation except Panoptic Quality that treats each ground truth object as an individual evaluation unit.

**Describe the solution you'd like**

Add connected component aware variants of existing MONAI semantic segmentation metrics. The proposed CC (Connected-Component-wise) Metrics operate as thin wrappers around existing MONAI metrics and:

- Decompose the ground truth foreground into connected components
- Assign each voxel to its nearest ground truth component via a Voronoi partition based on a single Euclidean distance/feature transform.
- Evaluate standard MONAI metrics inside each component specific region of interest.
- Supports aggregation modes (patient: mean over components per case &  overall: flat aggregation over all components)
- Integrate seamlessly with existing MONAI metrics such as DiceMetric, HausdorffDistanceMetric, SurfaceDistanceMetric, and SurfaceDiceMetric.

The implementation may be binary segmentation only first but coule be extended to multi-class approaches.

**Describe alternatives you've considered**

- Instance segmentation metrics. These require different model outputs and are not applicable to semantic segmentation pipelines. 
- Panoptic Quality offers a part of the solution but relies on a fixed and threshold dependant overlap-based matching and only consideres IoU as a metric.

**Additional context**

Reference implementation exists as a standalone library CC Metrics (https://github.com/alexanderjaus/CC-Metrics), published with peer reviewed validation.

The approach is described in “Every Component Counts: Rethinking the Measure of Success for Medical Semantic Segmentation in Multi Instance Segmentation Tasks”, AAAI 2025.

## Comments
### Comment by VijayVignesh1 at 2026-03-11T20:13:47Z
Hi @alexanderjaus,
I can start with integrating the per component parameter for the DiceScore metric, if that's okay.

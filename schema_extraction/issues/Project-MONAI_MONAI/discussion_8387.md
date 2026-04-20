# Discussion #8387: Unintuitive behaviour of `RandAffine` and `RandAffined`
**Repository:** Project-MONAI/MONAI
**Author:** MathijsdeBoer
**Created At:** 2025-03-12T09:38:09Z

## Description
The default behaviour of `RandAffine` and `RandAffined`'s `scale_range` parameter is to add a value of `1.0` to all elements of the argument. 

See the documentation:
- `scale_range` – scaling range with format matching rotate_range. it defines the range to randomly select the scale factor to translate for every spatial dims. A value of 1.0 is added to the result. This allows 0 to correspond to no change (i.e., a scaling of 1.0).

This, while clearly stated in the documentation, does seem a little unintuitive, and it has in fact caught me out, where I was simply passing `[0.9, 1.1]` to the constructor, causing strange warnings downstream in my random cropping step.

Would it be too disruptive to change this to a scale where a value of `1.0` is no change?

# Discussion #8495: Metric reduction when using DiceMetric or HausdorffDistanceMetric
**Repository:** Project-MONAI/MONAI
**Author:** CatarinaP98
**Created At:** 2025-06-22T18:35:02Z

## Description
Hi, 

I have a conceptual question, more than code-related. Hope that's ok!
I'm using MONAI to train and test a brain tumor segmentation model. I'm using DiceMetric + HausdorffDistanceMetric for evaluation, both of which have a reduction parameter. I understand what each type of metric reduction is doing, and my question is more about which one *should* be used.

I intend to report my results using the typical boxplots and a summary table containing the median/mean dice scores/hausdorff distances and the standard deviation for each class. To report the distributions and these statistics it seems appropriate to use reduction='none' so I can analyze the per-class distribution considering all samples. I feel like relying only on reduced metrics could be misleading, since we would be calculating the median of means, for example - would you agree?
However, the fact that the functions' default is reduction='mean' led me to question if calculating the mean is considered the standard or recommended approach to report these type of results, and why that would be.

I could not find in the literature any references to metric reduction for medical image segmentation applications, so I wanted to ask you if you could enlighten me on what is the correct approach? When is it appropriate to use reduction='none' vs reduction='mean' or 'mean_batch', and what are the advantages of each one? Would the best practice be to simply use reduction='none' followed by calculating statistics "manually"?

Thank you in advance for your time and for all the great work!

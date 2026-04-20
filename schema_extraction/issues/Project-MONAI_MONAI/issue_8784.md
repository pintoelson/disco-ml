# Issue #8784: Add Matthews Correlation Coefficient (MCC) Loss
**Repository:** Project-MONAI/MONAI
**Author:** kakumarabhishek
**Status:** closed
**Created At:** 2026-03-19T08:01:34Z

## Description
**Is your feature request related to a problem? Please describe.**
Medical image segmentation models trained with overlap-based loss functions like Dice and Tversky are susceptible to class imbalance, particularly when the foreground region is small relative to the background. These losses only consider TP, FP, and FN from the confusion matrix, ignoring true negatives (TN), which means they do not penalize misclassifications of background pixels. This can lead to suboptimal segmentation in datasets where background dominates the image.

**Describe the solution you'd like**
Add a Matthews Correlation Coefficient (MCC) loss function to monai.losses. The MCC loss uses all four entries of the confusion matrix (TP, TN, FP, FN) and has been shown to be effective for class-imbalanced segmentation. The loss is computed as 1 - MCC where MCC = (TP * TN - FP * FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN)), using soft confusion matrix entries to make it differentiable.                                                                                                                                                              

This was proposed in:

> K. Abhishek and G. Hamarneh, "Matthews Correlation Coefficient Loss for Deep Convolutional Networks: Application to Skin Lesion Segmentation," IEEE ISBI, 2021, pp. 225-229. https://doi.org/10.1109/ISBI48211.2021.9433782
                                                                                                                                                                                          
The paper has been cited 75 times, and the loss has also been adopted by the Segmentation Models PyTorch (smp) library. An implementation following MONAI conventions (supporting sigmoid, softmax, to_onehot_y, include_background, batch, reduction, etc.) along with unit tests is ready to submit as a PR.

**Describe alternatives you've considered**
- Using Dice loss or Tversky loss with tuned alpha/beta weights to mitigate class imbalance. These help but still fundamentally ignore TN.                                              
- Using compound losses like DiceCE or DiceFocal. These combine distance-based and overlap-based losses but add hyperparameter complexity without directly addressing all four confusion matrix entries.

**Additional context**
- Paper: https://doi.org/10.1109/ISBI48211.2021.9433782                                                                                                                                 
- Original code: https://github.com/kakumarabhishek/MCC-Loss
- [Segmentation Models PyTorch](https://smp.readthedocs.io/en/latest/index.html) adoption: the loss is available in smp as [smp.losses.MCCLoss](https://smp.readthedocs.io/en/latest/losses.html#mccloss)

## Comments
### Comment by aymuos15 at 2026-03-19T13:51:07Z
What do you mean by classes here? Isn't MCC generally used for binary problems? The paper also shows only binary segmentation right?

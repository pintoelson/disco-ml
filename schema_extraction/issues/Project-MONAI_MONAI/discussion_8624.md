# Discussion #8624: Forcing BCE for DiceCELoss when overlapping labels predictions
**Repository:** Project-MONAI/MONAI
**Author:** SebGoll
**Created At:** 2025-11-05T09:23:45Z

## Description
Hello,

I have encountered multiple projects in which I need to output multiple labels for a single voxel. In this case, I'd like to use the `DiceCELoss`, but forcing it to use the binary cross entropy loss instead of the cross entropy one (since each channel predicted is either on or off independently of the other channels). 
In the current state of `DiceCELoss`, it automatically choose to use either ce/bce based on the number of channels:
https://github.com/Project-MONAI/MONAI/blob/e72145ce852e1b59e2dbf6d57d3360979c2f9407/monai/losses/dice.py#L804

I wanted to see if there is an officially supported way to achieve the behavior described above before contributing.

Thank you

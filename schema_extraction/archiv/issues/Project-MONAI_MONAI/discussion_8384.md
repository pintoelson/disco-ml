# Discussion #8384: How to add a fully connected layer to the middle of an AutoEncoder model
**Repository:** Project-MONAI/MONAI
**Author:** karllandheer
**Created At:** 2025-03-11T16:37:56Z

## Description
Does anyone have an example of adding a fully connected layer to an AutoEncoder, or any MONAI model? There's a block called "Fully connected network", but I don't think that's quite what I want. What I want is to flatten the output from the encoder, add a linear layer if inputted size, and then reshape it to the input shape required by decoder. I'm sure someone has done this before, so any help would be greatly appreciated.

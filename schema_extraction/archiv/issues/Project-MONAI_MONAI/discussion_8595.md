# Discussion #8595: Does monai.engines.AdversarialTrainer Support torch.compile()?
**Repository:** Project-MONAI/MONAI
**Author:** Tyler-Slater
**Created At:** 2025-10-16T06:35:17Z

## Description
Apologies if this has been addressed before. I noticed that the SupervisedTrainer engine accepts a kwarg called "compile", but this kwarg is absent from AdversarialTrainer.

If I want to implement this manually by instantiating my generator and discriminator and calling torch.compile() on them before passing them into AdversarialTrainer, is this likely to cause issues?

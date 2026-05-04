# Discussion #8591: nnUNet Integration in MONAI ecosystem with MONet Bundle
**Repository:** Project-MONAI/MONAI
**Author:** SimoneBendazzoli93
**Created At:** 2025-10-01T09:07:48Z

## Description
Hi everyone!


Over the past year, I have been developing the [MONet Bundle](https://github.com/SimoneBendazzoli93/MONet-Bundle.git) to better integrate nnUNet within the MONAI ecosystem. The bundle enables:

- Direct nnUNet training integration within MAIA Core
- Support for MONAI Deploy, NVFlare (federated learning), and MONAI Label (active learning)

I have started contributing to the official MONAI repositories to bring this work into the main distributions (#8328 and [PR #543 in monai-deploy-app-sdk](https://github.com/Project-MONAI/monai-deploy-app-sdk/pull/543)).

I also recently presented the bundle at MICCAI 2025, demonstrating its NVFlare capabilities: [MONet-FL: Extending nnU-Net with MONAI for Clinical Federated Learning](https://link.springer.com/chapter/10.1007/978-3-032-05663-4_10).

Additionally, the following trained models, using the MONet bundle, are made available:

- [Brain tumor segmentation (BraTS 2025)](https://hub.docker.com/r/maiacloud/brats-x64-workstation-dgpu-linux-amd64)
- [Whole-body PET-CT lymphoma segmentation, adopting the MONet Bundle for Federated Learning with NVFlare](https://hub.docker.com/r/maiacloud/lymphoma-x64-workstation-dgpu-linux-amd64)

Both models can be included in the MONAI Model Zoo and can serve as examples for using the MONet Bundle.

Additionally, I have prepared some [Jupyter Notebook tutorials](https://github.com/SimoneBendazzoli93/MONet-Bundle) to help users get started with the MONet Bundle. These tutorials could be integrated into the MONAI Tutorial repository.

Next Steps / Proposal:
If the MONAI community finds this interesting, I would like to bring this work to the MONAI Core Working Group to coordinate and plan the full integration of the MONet Bundle into MONAI.

## Comments
### Comment by aylward at 2025-10-01T15:40:17Z
This is outstanding!   I have been following the MAIA effort, and it is a great example of a platform to support scientific research.   It would  be great to integrate the nnUNet/MONet bundle effort with the other nnUNet efforts in MONAI (Deploy and Core).

@rfloca (Human-AI WG / Label) @hshuaib90 (Deploy WG) and added you to Dev WG.

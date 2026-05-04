# Discussion #8743: Inquiry Regarding Registration Model Inference for Pre-to-Post Surgical Prediction
**Repository:** Project-MONAI/MONAI
**Author:** wangnanv5
**Created At:** 2026-02-18T13:07:05Z

## Description
Hello, I have a question regarding image registration that I would like to consult with you.
Currently, I possess paired binary images consisting of pre-operative and post-operative CT bone segmentation results for pectus excavatum surgery. My goal is to design a registration-based training framework where the model can generate the post-operative segmentation map solely by taking the pre-operative image as input during inference.
The objective of this experiment is relatively straightforward: to simulate minor deformations specifically in the skeletal structures surrounding the sternum. However, I have observed that all registration models available in MONAI require both a "moving image" and a "fixed image" (reference image) as inputs during the inference stage.
Could you please advise on how I can configure the workflow so that, during inference, the model only requires the pre-operative segmentation as input to predict the post-operative result?
I look forward to your valuable guidance.
Best regards,

## Comments
### Comment by omni-front at 2026-04-11T22:28:22Z
To better assist you, could you clarify a few details about your current setup? Specifically, which version of MONAI are you using, and have you considered any particular registration models within MONAI, such as VoxelMorph or others? Understanding your setup can help in suggesting a workflow that might fit your needs. Additionally, are you open to incorporating a different approach, such as a generative model, if registration models inherently require two inputs?

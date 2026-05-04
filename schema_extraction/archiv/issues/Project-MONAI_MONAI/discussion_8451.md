# Discussion #8451: MAISI ControlNet Semantic Mask Conditioning Training Issues
**Repository:** Project-MONAI/MONAI
**Author:** pshavela
**Created At:** 2025-05-13T07:33:04Z

## Description
Hello all,
firstly I would like to thank the MAISI team for their amazing work. 
I have been playing around with it and I am currently trying to reproduce the mask-conditioned  synthesis on a coronary CT dataset. I have trained the VAE and the MAISI diffusion model from scratch according to the tutorials, with great success. 

Unfortunately, I cannot get the ControlNet to converge, I have tried different learning rates (1e-5 and 1e-6), let it train
for more than 20000 steps, however, as the images below show the conditioning is not applied well enough.
I am also comparing the conditionally generated images at every epoch, but they yield similar results.

Does someone have some pointers on how to properly train the ControlNet with semantic masks and how to achieve comparable results?

![Screenshot from 2025-05-13 09-21-39](https://github.com/user-attachments/assets/adeb881d-6037-44e2-b0e8-3f2ae6316778)
![Screenshot from 2025-05-12 17-00-00](https://github.com/user-attachments/assets/d63ff891-984f-4a13-b34c-bb5f1d6d03e3)
![Screenshot from 2025-05-12 16-59-36](https://github.com/user-attachments/assets/64a39b4b-6589-461e-928e-3ac7859ab7db)

## Comments
### Comment by sara-create at 2025-06-26T09:56:41Z
@mazniashvili  Have you resolved your issue ? because I have the same problem now

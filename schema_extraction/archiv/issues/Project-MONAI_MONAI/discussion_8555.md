# Discussion #8555: Difference between self-attention and cross-attention in diffusion model unet
**Repository:** Project-MONAI/MONAI
**Author:** Ahmad-Omar-Ahsan
**Created At:** 2025-09-03T16:28:35Z

## Description
Hello everyone,

I am training a 2D conditional diffusion model on different labels. At the moment, I am only changing the number of classes parameter in the U-Net. I noticed that there is a `context-embed` argument, which goes along with the `with_conditioning`  argument. Going through the code, it looks like if with_conditioning is set to True, then it calls cross-attention; otherwise, it calls self-attention.

Which would be better, cross-attention or self-attention? Secondly,  if I decide to use cross-attention, what should the size of my context embedding be?

## Comments
### Comment by NabJa at 2025-09-04T07:20:42Z
Hi,

I haven't worked with this exact implementation. But generally, if you only have a few discrete labels, self-attention is usually fine, the model will learn to condition on those. Cross-attention is really good when your conditioning input has more structure (clinical features, text, etc.), since it lets the network focus dynamically instead of treating the label as a simple embedding.

For `context_embed`, typically you would pick something in line with your U-Net hidden dim (often the first channels entry, e.g. 64 or 128). If you use cross-attention, embed your labels into that size first.

Hope this helps :)

# Discussion #8381: How to access intermediate layer values
**Repository:** Project-MONAI/MONAI
**Author:** karllandheer
**Created At:** 2025-03-07T22:41:57Z

## Description
Hello, lets say I want to access some intermediate layer values in an autoencoder. Say the autoencoder is defined as this:
```

model = AutoEncoder(
        spatial_dims=2,
        in_channels=1,
        out_channels=1,
        channels=(4, 8, 16, 32, 64, 128),
        strides=(1, 2, 2, 2, 2, 2,),
        inter_channels=(64,32,16,8),
        inter_dilations = (2,2,2,2),
        num_res_units=0,
        num_inter_units=0
        
    )
```

and I am interested in accessing the values in inter_3 after running an image through the model, does anyone know how to do that?

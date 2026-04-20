# Discussion #8524: Usage of RandCropbyLabelClassesd--ERROR
**Repository:** Project-MONAI/MONAI
**Author:** sarvanichinthapalli
**Created At:** 2025-08-04T10:13:53Z

## Description
import numpy as np
import torch
from monai.transforms import RandCropByLabelClassesd

# Create random 3D image data (e.g., [512, 512, 91])
img_np = np.random.uniform(low=-3024, high=3071, size= (512, 512, 91)).astype(np.float32)

# Create label with only 0s and 1s, 1s are sparsely placed
lbl_np = np.zeros((512, 512, 91), dtype=np.uint8)
lbl_np[100:300, 100:200, 45:50] = 1  # Inject class 1 label sparsely

print("Image shape:", img_np.shape)
print("Label shape:", lbl_np.shape)

# Wrap in dict as expected by MONAI
data = {
    "image": img_np,
    "label": lbl_np
}

# Define cropping transform
crop_size = [32, 32, 91]  # height, width, depth

transform = RandCropByLabelClassesd(
    keys=["image", "label"],
    label_key="label",
    spatial_size=crop_size,
    num_classes=2,
    num_samples=1
)

# Apply transform
result = transform(data)[0].........




THrows error


Image shape: (512, 512, 91)
Label shape: (512, 512, 91)
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
[/tmp/ipython-input-4063268068.py](https://localhost:8080/#) in <cell line: 0>()
     31 
     32 # Apply transform
---> 33 result = transform(data)
     34 
     35 # Show shapes

6 frames
[/usr/local/lib/python3.11/dist-packages/monai/transforms/croppad/dictionary.py](https://localhost:8080/#) in __call__(self, data, lazy)
   1148     def __call__(self, data: Mapping[Hashable, Any], lazy: bool | None = None) -> list[dict[Hashable, torch.Tensor]]:
   1149         d = dict(data)
-> 1150         self.randomize(d.get(self.label_key), d.pop(self.indices_key, None), d.get(self.image_key))  # type: ignore
   1151 
   1152         # initialize returned list with shallow copy to preserve key ordering

[/usr/local/lib/python3.11/dist-packages/monai/transforms/croppad/dictionary.py](https://localhost:8080/#) in randomize(self, label, indices, image)
   1135         self, label: torch.Tensor, indices: list[NdarrayOrTensor] | None = None, image: torch.Tensor | None = None
   1136     ) -> None:
-> 1137         self.cropper.randomize(label=label, indices=indices, image=image)
   1138 
   1139     @LazyTransform.lazy.setter  # type: ignore

[/usr/local/lib/python3.11/dist-packages/monai/transforms/croppad/array.py](https://localhost:8080/#) in randomize(self, label, indices, image)
   1339         if _shape is None:
   1340             raise ValueError("label or image must be provided to infer the output spatial shape.")
-> 1341         self.centers = generate_label_classes_crop_centers(
   1342             self.spatial_size, self.num_samples, _shape, indices_, self.ratios, self.R, self.allow_smaller, self.warn
   1343         )

[/usr/local/lib/python3.11/dist-packages/monai/transforms/utils.py](https://localhost:8080/#) in generate_label_classes_crop_centers(spatial_size, num_samples, label_spatial_shape, indices, ratios, rand_state, allow_smaller, warn)
    751         center = unravel_index(indices_to_use[random_int], label_spatial_shape).tolist()
    752         # shift center to range of valid centers
--> 753         centers.append(correct_crop_centers(center, spatial_size, label_spatial_shape, allow_smaller))
    754 
    755     return ensure_tuple(centers)

[/usr/local/lib/python3.11/dist-packages/monai/transforms/utils.py](https://localhost:8080/#) in correct_crop_centers(centers, spatial_size, label_spatial_shape, allow_smaller)
    609 
    610     """
--> 611     spatial_size = fall_back_tuple(spatial_size, default=label_spatial_shape)
    612     if any(np.subtract(label_spatial_shape, spatial_size) < 0):
    613         if not allow_smaller:

[/usr/local/lib/python3.11/dist-packages/monai/utils/misc.py](https://localhost:8080/#) in fall_back_tuple(user_provided, default, func)
    294     """
    295     ndim = len(default)
--> 296     user = ensure_tuple_rep(user_provided, ndim)
    297     return tuple(  # use the default values if user provided is not valid
    298         user_c if func(user_c) else default_c for default_c, user_c in zip(default, user)

[/usr/local/lib/python3.11/dist-packages/monai/utils/misc.py](https://localhost:8080/#) in ensure_tuple_rep(tup, dim)
    220         return tuple(tup)
    221 
--> 222     raise ValueError(f"Sequence must have length {dim}, got {len(tup)}.")
    223 
    224 

ValueError: Sequence must have length 2, got 3.

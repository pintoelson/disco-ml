# Issue #8802: [BUG] ImageStats crashes when precomputed 'nda_croppeds' is provided
**Repository:** Project-MONAI/MONAI
**Author:** bluehyena
**Status:** closed
**Created At:** 2026-04-02T15:12:20Z

## Description
**Describe the bug**
`monai.auto3dseg.ImageStats.__call__()` crashes when precomputed 'nda_croppeds' is provided in the input mapping.

The current implementation only defines the local 'nda_croppeds' variable when the key is not present, but later always uses 'nda_croppeds' to populate 'cropped_shape' and intensity statistics. As a result, passing precomputed cropped foregrounds raises 'UnboundLocalError'.

**To Reproduce**
Steps to reproduce the behavior:

```python
import torch
from monai.auto3dseg.analyzer import ImageStats

analyzer = ImageStats(image_key="image")
analyzer(
    {
        "image": torch.arange(64.0, dtype=torch.float32).reshape(1, 4, 4, 4),
        "nda_croppeds": [torch.ones((2, 2, 2), dtype=torch.float32)],
    }
)
```

**Expected behavior**
```UnboundLocalError local variable 'nda_croppeds' referenced before assignment.```
If nda_croppeds is already provided, ImageStats should use it directly instead of recomputing foreground crops or crashing.

**Screenshots**

**Environment**
MONAI version: 1.5.2+87.g853f7023
MONAI rev id: 853f70236e42fe96fd690363fafd3a2d1e924c9a
Python version: 3.9.12
Pytorch version: 2.8.0+cpu
Numpy version: 1.24.3
Platform: Windows-10-10.0.22631-SP0
Has CUDA: False

**Additional context**
While investigating this path, I also confirmed that the analyzer-side grad-state leak discussed in #5889 is still reproducible on the current dev branch when exceptions are raised before the restore line.

I have a local fix prepared with regression tests for both the nda_croppeds crash and the grad state leak.

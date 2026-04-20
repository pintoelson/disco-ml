# Issue #8789: FutureWarning: `cuda.cudart` module is deprecated
**Repository:** Project-MONAI/MONAI
**Author:** vmiller987
**Status:** closed
**Created At:** 2026-03-23T15:03:35Z

## Description
**Describe the bug**
`monai.networks.trt_compiler` (line 42) imports `cuda.cudart` via `optional_import`, which triggers a `FutureWarning` with `cuda-bindings>=12.6`:

```bash
<frozen importlib._bootstrap_external>:1325: FutureWarning: The cuda.cudart module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.runtime module instead.
```

The import should be updated to use `cuda.bindings.runtime` with a fallback to `cuda.cudart`.

**To Reproduce**
1. Install MONAI with `cuda-bindings >= 12.6` (e.g. pulled in by PyTorch 2.10)
2. `import monai` 
3. Warning is emitted during module load.

```bash
(venv) [vmiller@gluskap]$ python -c "import monai"
<frozen importlib._bootstrap_external>:1325: FutureWarning: The cuda.cudart module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.runtime module instead.
(venv) [vmiller@gluskap]$ 
```

**Expected behavior**
No deprecation warning. `trt_compiler.py` should prefer `cuda.bindings.runtime` and fall back to `cuda.cudart` only if the new module is unavailable.

**Suggested fix**
In `monai/networks/trt_compiler.py`, line 42:

```python
# Current
cudart, _ = optional_import("cuda.cudart")

# Proposed
cudart, cudart_available = optional_import("cuda.bindings.runtime")
if not cudart_available:
    cudart, _ = optional_import("cuda.cudart")
```

**Environment**

Ensuring you use the relevant python executable, please paste the output of:

```bash
(venv) [vmiller@gluskap]$ python -c "import monai; monai.config.print_debug_info()"
<frozen importlib._bootstrap_external>:1325: FutureWarning: The cuda.cudart module is deprecated and will be removed in a future release, please switch to use the cuda.bindings.runtime module instead.
================================
Printing MONAI config...
================================
MONAI version: 1.5.2
Numpy version: 2.4.3
Pytorch version: 2.10.0+cu128
MONAI flags: HAS_EXT = False, USE_COMPILED = False, USE_META_DICT = False
MONAI rev id: d18565fb3e4fd8c556707f91ac280a2dc3f681c1
MONAI __file__: /home/<username>/Work/frag-ct/.venv/lib/python3.13/site-packages/monai/__init__.py

Optional dependencies:
Pytorch Ignite version: NOT INSTALLED or UNKNOWN VERSION.
ITK version: NOT INSTALLED or UNKNOWN VERSION.
Nibabel version: 5.4.2
scikit-image version: 0.26.0
scipy version: 1.17.1
Pillow version: 12.1.1
Tensorboard version: NOT INSTALLED or UNKNOWN VERSION.
gdown version: NOT INSTALLED or UNKNOWN VERSION.
TorchVision version: 0.25.0+cu128
tqdm version: 4.67.3
lmdb version: NOT INSTALLED or UNKNOWN VERSION.
psutil version: 7.2.2
pandas version: 3.0.1
einops version: 0.8.2
transformers version: NOT INSTALLED or UNKNOWN VERSION.
mlflow version: NOT INSTALLED or UNKNOWN VERSION.
pynrrd version: 1.1.3
clearml version: NOT INSTALLED or UNKNOWN VERSION.

For details about installing the optional dependencies, please visit:
    https://docs.monai.io/en/latest/installation.html#installing-the-recommended-dependencies


================================
Printing system config...
================================
System: Linux
Linux version: Red Hat Enterprise Linux 9.7 (Plow)
Platform: Linux-5.14.0-611.38.1.el9_7.x86_64-x86_64-with-glibc2.34
Processor: x86_64
Machine: x86_64
Python version: 3.13.11
Process name: python
Command: ['python', '-c', 'import monai; monai.config.print_debug_info()']
Open files: []
Num physical CPUs: 24
Num logical CPUs: 48
Num usable CPUs: 48
CPU usage (%): [28.1, 18.3, 10.9, 45.9, 35.3, 38.9, 5.9, 5.4, 4.3, 4.3, 5.4, 3.8, 7.5, 7.0, 5.9, 5.9, 4.4, 5.9, 7.0, 4.9, 6.5, 4.3, 4.3, 7.6, 42.7, 16.7, 8.7, 52.2, 9.2, 47.6, 3.8, 4.8, 4.3, 5.9, 5.4, 4.3, 5.9, 6.5, 6.5, 5.9, 5.9, 5.9, 5.4, 4.9, 4.3, 5.4, 4.3, 7.0]
CPU freq. (MHz): 3148
Load avg. in last 1, 5, 15 mins (%): [7.1, 6.4, 6.8]
Disk usage (%): 50.0
Avg. sensor temp. (Celsius): UNKNOWN for given OS
Total physical memory (GB): 754.4
Available memory (GB): 518.2
Used memory (GB): 236.2

================================
Printing GPU config...
================================
Num GPUs: 7
Has CUDA: True
CUDA version: 12.8
cuDNN enabled: True
NVIDIA_TF32_OVERRIDE: None
TORCH_ALLOW_TF32_CUBLAS_OVERRIDE: None
cuDNN version: 91002
Current device: 0
Library compiled for CUDA architectures: ['sm_70', 'sm_75', 'sm_80', 'sm_86', 'sm_90', 'sm_100', 'sm_120']
GPU 0 Name: NVIDIA GeForce RTX 4090
GPU 0 Is integrated: False
GPU 0 Is multi GPU board: False
GPU 0 Multi processor count: 128
GPU 0 Total memory (GB): 23.5
GPU 0 CUDA capability (maj.min): 8.9
GPU 1 Name: NVIDIA GeForce RTX 4090
GPU 1 Is integrated: False
GPU 1 Is multi GPU board: False
GPU 1 Multi processor count: 128
GPU 1 Total memory (GB): 23.5
GPU 1 CUDA capability (maj.min): 8.9
GPU 2 Name: NVIDIA GeForce RTX 4090
GPU 2 Is integrated: False
GPU 2 Is multi GPU board: False
GPU 2 Multi processor count: 128
GPU 2 Total memory (GB): 23.5
GPU 2 CUDA capability (maj.min): 8.9
GPU 3 Name: NVIDIA GeForce RTX 4090
GPU 3 Is integrated: False
GPU 3 Is multi GPU board: False
GPU 3 Multi processor count: 128
GPU 3 Total memory (GB): 23.5
GPU 3 CUDA capability (maj.min): 8.9
GPU 4 Name: NVIDIA GeForce RTX 4090
GPU 4 Is integrated: False
GPU 4 Is multi GPU board: False
GPU 4 Multi processor count: 128
GPU 4 Total memory (GB): 23.5
GPU 4 CUDA capability (maj.min): 8.9
GPU 5 Name: NVIDIA GeForce RTX 4090
GPU 5 Is integrated: False
GPU 5 Is multi GPU board: False
GPU 5 Multi processor count: 128
GPU 5 Total memory (GB): 23.5
GPU 5 CUDA capability (maj.min): 8.9
GPU 6 Name: NVIDIA GeForce RTX 4090
GPU 6 Is integrated: False
GPU 6 Is multi GPU board: False
GPU 6 Multi processor count: 128
GPU 6 Total memory (GB): 23.5
GPU 6 CUDA capability (maj.min): 8.9
(frag-ct) [vmiller@gluskap frag-ct]$ 
```

**Additional context**
The `cuda.cudart` module will be removed in a future `cuda-bindings` release, at which point this import will fail entirely rather than just warn.

# Issue #8735: AutoencoderKlMaisi transfers to cuda even if input and model are on CPU
**Repository:** Project-MONAI/MONAI
**Author:** coolteemf
**Status:** closed
**Created At:** 2026-02-09T18:56:53Z

## Description
**Describe the bug**

AutoencoderKlMaisi transfers to cuda even if input and model are on CPU

Line 228 in `monai/apps/generation/maisi/networks/autoencoderkl_maisi.py`: `x = x.to("cuda", non_blocking=True)`

```
    def _concatenate_tensors(self, outputs: list[torch.Tensor], split_size: int, padding: int) -> torch.Tensor:
        slices = [slice(None)] * 5
        for i in range(self.num_splits):
            slices[self.dim_split + 2] = slice(None, split_size) if i == 0 else slice(padding, padding + split_size)
            outputs[i] = outputs[i][tuple(slices)]

        if self.print_info:
            for i in range(self.num_splits):
                logger.info(f"Output {i + 1}/{len(outputs)} size after: {outputs[i].size()}")

        if max(outputs[0].size()) < 500:
            x = torch.cat(outputs, dim=self.dim_split + 2)
        else:
            x = outputs[0].clone().to("cpu", non_blocking=True)
            outputs[0] = torch.Tensor(0)
            _empty_cuda_cache(self.save_mem)
            for k in range(len(outputs) - 1):
                x = torch.cat((x, outputs[k + 1].cpu()), dim=self.dim_split + 2)
                outputs[k + 1] = torch.Tensor(0)
                _empty_cuda_cache(self.save_mem)
                gc.collect()
                if self.print_info:
                    logger.info(f"MaisiConvolution concat progress: {k + 1}/{len(outputs) - 1}.")

            x = x.to("cuda", non_blocking=True)
        return x
```

**To Reproduce**

Pass a large CPU tensor to autoencoder:

Example:

```
from monai.apps.generation.maisi.networks.autoencoderkl_maisi import AutoencoderKlMaisi

autoencoder_def = {
        "spatial_dims": 3,
        "in_channels": 1,
        "out_channels": 1,
        "latent_channels": 4,
        "num_channels": [
            64,
            128,
            256
        ],
        "num_res_blocks": [2,2,2],
        "norm_num_groups": 32,
        "norm_eps": 1e-06,
        "attention_levels": [
            False,
            False,
            False
        ],
        "with_encoder_nonlocal_attn": False,
        "with_decoder_nonlocal_attn": False,
        "use_checkpointing": False,
        "use_convtranspose": False,
        "norm_float16": True,
        "num_splits": 4,
        "dim_split": 1
    }

ae = AutoencoderKlMaisi(**autoencoder_def)

input = torch.rand(1,1,512,512,512, device="cpu")
output = ae.encode_stage_2_inputs(input) #<- transfer to CUDA happens in this block, will fail if you have less than 80G VRAM
```

```
 File "/home/<username>/.cache/pypoetry/virtualenvs/nv-generate-ctmr-7dMRnJh0-py3.12/lib/python3.12/site-packages/monai/apps/generation/maisi/networks/autoencoderkl_maisi.py", line 274, in forward
    x = self._concatenate_tensors(outputs, split_size_out, padding_s)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/<username>/.cache/pypoetry/virtualenvs/nv-generate-ctmr-7dMRnJh0-py3.12/lib/python3.12/site-packages/monai/apps/generation/maisi/networks/autoencoderkl_maisi.py", line 228, in _concatenate_tensors
    x = x.to("cuda", non_blocking=True)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
torch.OutOfMemoryError: CUDA out of memory. Tried to allocate 32.00 GiB. GPU 0 has a total capacity of 23.52 GiB of which 23.05 GiB is free. Including non-PyTorch memory, this process has 386.00 MiB memory in use. Of the allocated memory 0 bytes is allocated by PyTorch, and 0 bytes is reserved by PyTorch but unallocated. If reserved but unallocated memory is large try setting PYTORCH_ALLOC_CONF=expandable_segments:True to avoid fragmentation.  See documentation for Memory Management  (https://pytorch.org/docs/stable/notes/cuda.html#environment-variables)
```

**Expected behavior**

No transfer to CUDA if input and autoencoder are on CPU.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment**

Ensuring you use the relevant python executable, please paste the output of:

```
python -c "import monai; monai.config.print_debug_info()"
```

```
================================
Printing MONAI config...
================================
MONAI version: 1.6.dev2605
Numpy version: 2.4.2
Pytorch version: 2.10.0+cu128
MONAI flags: HAS_EXT = False, USE_COMPILED = False, USE_META_DICT = False
MONAI rev id: fa78faee811526ddafb3df6160ecfafad1b75236
MONAI __file__: /home/<username>/.cache/pypoetry/virtualenvs/nv-generate-ctmr-7dMRnJh0-py3.12/lib/python3.12/site-packages/monai/__init__.py

Optional dependencies:
Pytorch Ignite version: NOT INSTALLED or UNKNOWN VERSION.
ITK version: NOT INSTALLED or UNKNOWN VERSION.
Nibabel version: 5.3.3
scikit-image version: 0.26.0
scipy version: 1.17.0
Pillow version: 12.1.0
Tensorboard version: NOT INSTALLED or UNKNOWN VERSION.
gdown version: NOT INSTALLED or UNKNOWN VERSION.
TorchVision version: NOT INSTALLED or UNKNOWN VERSION.
tqdm version: 4.67.2
lmdb version: NOT INSTALLED or UNKNOWN VERSION.
psutil version: 7.2.2
pandas version: NOT INSTALLED or UNKNOWN VERSION.
einops version: 0.8.2
transformers version: NOT INSTALLED or UNKNOWN VERSION.
mlflow version: NOT INSTALLED or UNKNOWN VERSION.
pynrrd version: NOT INSTALLED or UNKNOWN VERSION.
clearml version: NOT INSTALLED or UNKNOWN VERSION.

For details about installing the optional dependencies, please visit:
    https://monai.readthedocs.io/en/latest/installation.html#installing-the-recommended-dependencies


================================
Printing system config...
================================
System: Linux
Linux version: Ubuntu 22.04.4 LTS
Platform: Linux-6.8.0-90-generic-x86_64-with-glibc2.35
Processor: x86_64
Machine: x86_64
Python version: 3.12.2
Process name: python
Command: ['/home/<username>/.cache/pypoetry/virtualenvs/nv-generate-ctmr-7dMRnJh0-py3.12/bin/python', '-X', 'frozen_modules=off', '/home/<username>/.vscode-server/extensions/ms-python.debugpy-2025.18.0-linux-x64/bundled/libs/debugpy/adapter/../../debugpy/launcher/../../debugpy', '--connect', '127.0.0.1:60989', '--configure-qt', 'none', '--adapter-access-token', 'f4c6234902178d2181c82c866b73559d99aa3064def2e79e4fd9e18959200b21', '-m', 'scripts.outpaint_inference', '-e', 'configs/environment_rflow-ct.json', '-c', 'configs/config_infer_80g_512x512x512.json', '-t', 'configs/config_network_rflow.json', '-i', './heart_aligned.nii.gz', '--mask_path', 'combined_labelmap.nii.gz', '--use_cpu']
Open files: []
Num physical CPUs: 16
Num logical CPUs: 32
Num usable CPUs: 32
CPU usage (%): [0.8, 1.5, 0.7, 5.2, 1.8, 3.0, 1.2, 1.4, 2.8, 3.5, 2.5, 2.7, 1.4, 0.5, 2.6, 2.8, 2.8, 2.3, 2.5, 1.5, 2.2, 0.3, 2.0, 1.8, 0.9, 1.1, 1.3, 0.9, 2.1, 2.9, 0.8, 0.7]
CPU freq. (MHz): 2198
Load avg. in last 1, 5, 15 mins (%): [0.4, 1.5, 2.3]
Disk usage (%): 48.0
Avg. sensor temp. (Celsius): UNKNOWN for given OS
Total physical memory (GB): 125.7
Available memory (GB): 80.6
Used memory (GB): 45.0

================================
Printing GPU config...
================================
Num GPUs: 1
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
```


**Additional context**

Rest of the file already seems to handle CPU input correctly:

`return input.to("cuda", non_blocking=True) if input_type == "cuda" else input`

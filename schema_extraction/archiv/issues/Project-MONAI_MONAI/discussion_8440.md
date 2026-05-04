# Discussion #8440: MONAI Deploy Tutorial setup and execution issues
**Repository:** Project-MONAI/MONAI
**Author:** learnbanjo
**Created At:** 2025-05-07T06:47:29Z

## Description
Following https://docs.monai.io/projects/monai-deploy-app-sdk/en/latest/getting_started/tutorials/simple_app.html# Executing from Shell ,  to setup and execute app, and run into multiple failures. 

I'm using MacBook Pro 2019 ( Intel CPU). Does MONAI Deploy require CUDA and it can't be run on Mac?

Problem 1: conda setup error
`conda create -n monai python=3.9 pytorch torchvision jupyterlab cudatoolkit=12.2 -c pytorch -c conda-forge`
failed with following error:
`PackagesNotFoundError: The following packages are not available from current channels:
  - cudatoolkit=12.2*`
Was able to proceed by removing "cudatoolkit=12.2" from the line

Problem 2:  executing the app failed with property not found. Checking doc, there's no such property in API
`python examples/apps/simple_imaging_app/app.py`

error:
`Traceback (most recent call last):
  File "/Users/jerryhsu/Workspace/monai-deploy-app-sdk/examples/apps/simple_imaging_app/app.py", line 15, in <module>
    from gaussian_operator import GaussianOperator
  File "/Users/jerryhsu/Workspace/monai-deploy-app-sdk/examples/apps/simple_imaging_app/gaussian_operator.py", line 14, in <module>
    from monai.deploy.core import ConditionType, Fragment, Operator, OperatorSpec
ImportError: cannot import name 'ConditionType' from 'monai.deploy.core' (/opt/anaconda3/envs/monai/lib/python3.9/site-packages/monai/deploy/core/__init__.py)
`

## Comments
### Comment by learnbanjo at 2025-05-07T07:39:45Z
I think I found my answer. Mac is not supported the toolkit requires requires NVIDIA driver

"Prerequisites

This SDK depends on [NVIDIA Holoscan SDK](https://pypi.org/project/holoscan/) for its core implementation as well as its CLI, hence inherits its prerequisites, e.g. Ubuntu 22.04 with glibc 2.35 on X86-64 and NVIDIA dGPU drivers version 535 or above.

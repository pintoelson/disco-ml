# Issue #8737: `apex.contrib.clip_grad.clip_grad_norm_` crashes with PyTorch 2.10
**Repository:** Project-MONAI/MONAI
**Author:** KumoLiu
**Status:** open
**Created At:** 2026-02-11T15:21:51Z

## Description
**Environment**
NGC Base Image: nvcr.io/nvidia/pytorch:25.12-py3
PyTorch: 2.10.0a0+b4e4ee81d3.nv25.12
CUDA: 13
Python: 3.12
apex: as shipped in NGC 25.12

This happens because apex's multi_tensor_applier attempts to access the raw data pointer of gradient tensors, but in PyTorch 2.10 some tensors (e.g., those with lazy/functional storage) no longer expose a traditional storage, causing the operation to fail.

```

[2026-02-11T15:17:23.401Z] ======================================================================

[2026-02-11T15:17:23.401Z] ERROR: test_ensemble (tests.integration.test_auto3dseg_ensemble.TestEnsembleBuilder.test_ensemble)

[2026-02-11T15:17:23.401Z] ----------------------------------------------------------------------

[2026-02-11T15:17:23.401Z] Traceback (most recent call last):

[2026-02-11T15:17:23.401Z]   File "/home/jenkins/agent/workspace/YunLiu-Monai-pytorch-versions/monai/utils/misc.py", line 894, in run_cmd

[2026-02-11T15:17:23.401Z]     return subprocess.run(cmd_list, **kwargs)

[2026-02-11T15:17:23.401Z]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

[2026-02-11T15:17:23.401Z]   File "/usr/lib/python3.12/subprocess.py", line 571, in run

[2026-02-11T15:17:23.401Z]     raise CalledProcessError(retcode, process.args,

[2026-02-11T15:17:23.401Z] subprocess.CalledProcessError: Command '['python', '/tmp/tmp7gsbt0qp/workdir/dints_0/scripts/train.py', 'run', "--config_file='/tmp/tmp7gsbt0qp/workdir/dints_0/configs/hyper_parameters.yaml,/tmp/tmp7gsbt0qp/workdir/dints_0/configs/hyper_parameters_search.yaml,/tmp/tmp7gsbt0qp/workdir/dints_0/configs/network.yaml,/tmp/tmp7gsbt0qp/workdir/dints_0/configs/network_search.yaml,/tmp/tmp7gsbt0qp/workdir/dints_0/configs/transforms_infer.yaml,/tmp/tmp7gsbt0qp/workdir/dints_0/configs/transforms_train.yaml,/tmp/tmp7gsbt0qp/workdir/dints_0/configs/transforms_validate.yaml'", '--training#num_images_per_batch=2', '--training#num_epochs=2', '--training#num_epochs_per_validation=1']' returned non-zero exit status 1.

[2026-02-11T15:17:23.401Z] 

[2026-02-11T15:17:23.401Z] The above exception was the direct cause of the following exception:

[2026-02-11T15:17:23.401Z] 

[2026-02-11T15:17:23.401Z] Traceback (most recent call last):

[2026-02-11T15:17:23.401Z]   File "/home/jenkins/agent/workspace/YunLiu-Monai-pytorch-versions/tests/integration/test_auto3dseg_ensemble.py", line 167, in test_ensemble

[2026-02-11T15:17:23.401Z]     algo.train(_train_param)

[2026-02-11T15:17:23.401Z]   File "/tmp/tmpiqosipwp/workdir/algorithm_templates/dints/scripts/algo.py", line 497, in train

[2026-02-11T15:17:23.401Z]   File "/home/jenkins/agent/workspace/YunLiu-Monai-pytorch-versions/monai/apps/auto3dseg/bundle_gen.py", line 277, in _run_cmd

[2026-02-11T15:17:23.401Z]     return run_cmd(cmd.split(), run_cmd_verbose=True, env=ps_environ, check=True)

[2026-02-11T15:17:23.401Z]            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

[2026-02-11T15:17:23.401Z]   File "/home/jenkins/agent/workspace/YunLiu-Monai-pytorch-versions/monai/utils/misc.py", line 898, in run_cmd

[2026-02-11T15:17:23.401Z]     raise RuntimeError(f"subprocess call error {e.returncode}: {errors}, {output}") from e

[2026-02-11T15:17:23.401Z] RuntimeError: subprocess call error 1: ERROR:torch_tensorrt._utils:CUDA 13 is not currently supported for TRT-LLM plugins. Please install pytorch with CUDA 12.x support

[2026-02-11T15:17:23.401Z] monai.transforms.spatial.dictionary Orientationd.__init__:labels: Current default value of argument `labels=(('L', 'R'), ('P', 'A'), ('I', 'S'))` was changed in version None from `labels=(('L', 'R'), ('P', 'A'), ('I', 'S'))` to `labels=None`. Default value changed to None meaning that the transform now uses the 'space' of a meta-tensor, if applicable, to determine appropriate axis labels.

[2026-02-11T15:17:23.401Z] The filesystem tracking backend (e.g., './mlruns') will be deprecated in February 2026. Consider transitioning to a database backend (e.g., 'sqlite:///mlflow.db') to take advantage of the latest MLflow features. See https://github.com/mlflow/mlflow/issues/18534 for more details and migration guidance. For migrating existing data, https://github.com/mlflow/mlflow-export-import can be used.

[2026-02-11T15:17:23.401Z] 2026/02/11 14:47:11 INFO mlflow.tracking.fluent: Experiment with name 'Auto3DSeg' does not exist. Creating a new experiment.

[2026-02-11T15:17:23.401Z] 
[2026-02-11T15:17:23.401Z] dints_0 - training ...:   0%|          | 0/2 [00:00<?, ?round/s]
[2026-02-11T15:17:23.401Z] dints_0 - training ...:   0%|          | 0/2 [00:01<?, ?round/s]

[2026-02-11T15:17:23.401Z] Traceback (most recent call last):

[2026-02-11T15:17:23.401Z]   File "/tmp/tmp7gsbt0qp/workdir/dints_0/scripts/train.py", line 1001, in <module>

[2026-02-11T15:17:23.401Z]     fire.Fire()

[2026-02-11T15:17:23.401Z]   File "/usr/local/lib/python3.12/dist-packages/fire/core.py", line 135, in Fire

[2026-02-11T15:17:23.401Z]     component_trace = _Fire(component, args, parsed_flag_args, context, name)

[2026-02-11T15:17:23.401Z]                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

[2026-02-11T15:17:23.401Z]   File "/usr/local/lib/python3.12/dist-packages/fire/core.py", line 468, in _Fire

[2026-02-11T15:17:23.401Z]     component, remaining_args = _CallAndUpdateTrace(

[2026-02-11T15:17:23.401Z]                                 ^^^^^^^^^^^^^^^^^^^^

[2026-02-11T15:17:23.401Z]   File "/usr/local/lib/python3.12/dist-packages/fire/core.py", line 684, in _CallAndUpdateTrace

[2026-02-11T15:17:23.401Z]     component = fn(*varargs, **kwargs)

[2026-02-11T15:17:23.401Z]                 ^^^^^^^^^^^^^^^^^^^^^^

[2026-02-11T15:17:23.401Z]   File "/tmp/tmp7gsbt0qp/workdir/dints_0/scripts/train.py", line 606, in run

[2026-02-11T15:17:23.401Z]     clip_grad_norm_(model.parameters(), 0.5)

[2026-02-11T15:17:23.401Z]   File "/usr/local/lib/python3.12/dist-packages/apex/contrib/clip_grad/clip_grad.py", line 80, in clip_grad_norm_

[2026-02-11T15:17:23.401Z]     multi_tensor_applier(

[2026-02-11T15:17:23.401Z]   File "/usr/local/lib/python3.12/dist-packages/apex/multi_tensor_apply/multi_tensor_apply.py", line 27, in __call__

[2026-02-11T15:17:23.401Z]     return op(self.chunk_size,

[2026-02-11T15:17:23.401Z]            ^^^^^^^^^^^^^^^^^^^

[2026-02-11T15:17:23.401Z] RuntimeError: Cannot access data pointer of Tensor that doesn't have storage

[2026-02-11T15:17:23.401Z] , 
```

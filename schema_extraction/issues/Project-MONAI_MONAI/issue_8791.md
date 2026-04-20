# Issue #8791: ModuleNotFoundError: No module named 'backports'
**Repository:** Project-MONAI/MONAI
**Author:** ytl0623
**Status:** closed
**Created At:** 2026-03-25T07:05:46Z

## Description
[https://github.com/Project-MONAI/MONAI/actions/runs/23528202168/job/68486083838?pr=8790](https://github.com/Project-MONAI/MONAI/actions/runs/23528202168/job/68486083838?pr=8790)

**Describe the bug**
```
Traceback (most recent call last):
  File "/home/runner/work/MONAI/MONAI/setup.py", line 21, in <module>
    from setuptools import find_packages, setup
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/setuptools/__init__.py", line 18, in <module>
    from setuptools.dist import Distribution
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/setuptools/dist.py", line 46, in <module>
    from . import _reqs
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/setuptools/_reqs.py", line 1, in <module>
    import setuptools.extern.jaraco.text as text
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/setuptools/_vendor/jaraco/text/__init__.py", line 12, in <module>
    from setuptools.extern.jaraco.context import ExceptionTrap
  File "/opt/hostedtoolcache/Python/3.10.20/x64/lib/python3.10/site-packages/setuptools/_vendor/jaraco/context/__init__.py", line 18, in <module>
    from backports import tarfile
ModuleNotFoundError: No module named 'backports'
```

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Install '....'
3. Run commands '....'

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment**

Ensuring you use the relevant python executable, please paste the output of:

```
python -c "import monai; monai.config.print_debug_info()"
```

**Additional context**
Add any other context about the problem here.

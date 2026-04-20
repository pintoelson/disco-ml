# Issue #8832: Raise different exception when hash value of download is wrong
**Repository:** Project-MONAI/MONAI
**Author:** e-mny
**Status:** open
**Created At:** 2026-04-18T04:32:39Z

## Description
> One thing we may want to change later is to raise a different exception when the hash fails [here](https://github.com/Project-MONAI/MONAI/blob/57fdd594ac905ab2ea778aa4bb79ccd9a0a03b22/monai/apps/utils.py#L271). It should maybe raise something specific to this and so isn't suppressed by `skip_if_download_fails`. Let's not worry about that in this PR yet however.

_Originally posted by @ericspod in https://github.com/Project-MONAI/MONAI/issues/8699#issuecomment-3766056855_

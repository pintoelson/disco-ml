# Issue #8813: Pybind11 Missing When Installing Pytype
**Repository:** Project-MONAI/MONAI
**Author:** ericspod
**Status:** closed
**Created At:** 2026-04-09T19:50:46Z

## Description
**Describe the bug**
`pybind11` is a requirement for `pytype` but somehow is now being missed as an explicit requirement. This has to be added back in explicitly in places now.

# Issue #8806: [EHNANCEMENT] Better Performance For engines/utils.py
**Repository:** Project-MONAI/MONAI
**Author:** benediktjohannes
**Status:** open
**Created At:** 2026-04-04T22:51:33Z

## Description
I‘m creating this so that we don’t forget about the enhancement proposal by @ericspod in #8747 (thank you Eric for the Suggestion!)

## Comments
### Comment by Zeesejo at 2026-04-17T19:56:23Z
Hi @benediktjohannes and @ericspod, I'd like to implement the suggestion from @ericspod in #8747.

My plan:
1. In `PrepareBatchExtraInput.__call__` (`monai/engines/utils.py`), replace the `args_` list + `for` loop with a direct generator expression passed to `tuple()`, and replace `kwargs_.update({k: ...})` with a dict comprehension — exactly as @ericspod suggested in the resolved review comment on #8747.
2. Add/update the existing unit tests in `tests/engines/test_utils.py` to cover the refactored path.

This is a non-breaking refactor (semantically identical, slightly more efficient). Does this match what you had in mind?
### Comment by ericspod at 2026-04-19T22:40:00Z
Hi @Zeesejo I'm fine for you to go ahead, I should see the PR once it's ready.
### Comment by benediktjohannes at 2026-04-19T23:29:14Z
Perfect, thank you!

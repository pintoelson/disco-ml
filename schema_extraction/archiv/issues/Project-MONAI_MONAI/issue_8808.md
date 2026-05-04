# Issue #8808: Add EmbeddingCollapseMetric: detect representational collapse in medical imaging embeddings
**Repository:** Project-MONAI/MONAI
**Author:** ekansh-arora0
**Status:** open
**Created At:** 2026-04-07T00:55:36Z

## Description
**Is your feature request related to a problem? Please describe.**


When fine-tuning or deploying foundation models on new domains, model embeddings can silently lose discriminative power, known as representational collapse. There is currently no metric in MONAI to quantitatively detect this. Users have no way to tell whether their embeddings are still meaningfully separating classes or have degenerated into a narrow subspace, leading to misleading downstream task performance that only becomes apparent after costly training cycles.

## Describe the solution you'd like

I'm implementing `EmbeddingCollapseMetric`, a new metric class. It computes a suite of collapse indicators from embeddings
and optional class labels:

- Centroid cosine similarity — cosine similarity between L2-normalised class
  centroids. 1.0 = centroids identical (full collapse).
- SVD effective rank score — based on Roy & Vetterli (2007). Detects
  dimensional collapse: a model using 6 of 768 dimensions scores near 1.0.
- Per-class SVD — effective rank computed separately per class. Detects
  asymmetric collapse where one class collapses while the other stays rich.
- Linear CKA — Kornblith et al. (2019). Measures representation similarity
  between source and target domains for cross-domain shift detection.
- Silhouette score — inter-class separation via cosine distance.
- Leave-one-out centroid stability — std-dev of centroid similarity under
  LOO resampling. Validates point estimates on small n (e.g. n=14 slides).

Results are returned as a plain `dict`. A `linear_probe_accuracy()` utility
method (sklearn via `optional_import`) is included for downstream validation.

Dependencies: torch + numpy only in core. sklearn and matplotlib
are imported lazily via optional_import.

The class follows the `FIDMetric` / `MMDMetric` architectural pattern:
tensor-in, tensor-out, no I/O side effects.

## Describe alternatives you've considered

-FIDMetric measures distributional shift but requires a large reference
  set and doesn't decompose by class or detect dimensional collapse.
- MMDMetric is a two-sample test, not a collapse detector.
- Silhouette score alone is O(n²), requires sklearn, and doesn't detect
  dimensional collapse or cross-domain shift.

`EmbeddingCollapseMetric` is complementary to both, answering a different
question: not "are these distributions different?" but "has the model lost the
ability to distinguish classes?"

## Additional context

I have a working prototype and will open a draft PR against `dev` imminently.

References:
- Roy & Vetterli (2007). The effective rank. *EUSIPCO*.
- Kornblith et al. (2019). Similarity of neural network representations revisited. *ICML*.
- Hua et al. (2021). On feature decorrelation in self-supervised learning. *ICCV*.

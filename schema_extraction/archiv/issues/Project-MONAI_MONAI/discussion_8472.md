# Discussion #8472: `decollate_batch` different behavior between numpy and torch?
**Repository:** Project-MONAI/MONAI
**Author:** arthurdjn
**Created At:** 2025-06-03T13:11:38Z

## Description
I am trying to understand why the behavior of the `decollate_batch` is different with numpy and torch? The strategy for decollating batches is indeed different, e.g.

```python
# With tensor
decollate_batch({"value": torch.tensor([[1, 1, 1, 1], [2, 2, 2, 2]])})
# [{'value': tensor([1, 1, 1, 1])}, {'value': tensor([2, 2, 2, 2])}]

# With numpy
decollate_batch({"value": np.array([[1, 1, 1, 1], [2, 2, 2, 2]])})
# [{'value': [1, 2]}, {'value': [1, 2]}, {'value': [1, 2]}, {'value': [1, 2]}]

# With lists
decollate_batch({"value": [[1, 1, 1, 1], [2, 2, 2, 2]]})
# [{'value': [1, 2]}, {'value': [1, 2]}, {'value': [1, 2]}, {'value': [1, 2]}]
```

I would expect at least to have the same behavior with numpy and torch but this is not the case. In fact I though the `decollate_batch` would expect "batched" data where the first dim corresponds to the batch size, so the output of `decollate_batch` would be of the same length as the batch size -- but this is not the case for numpy arrays / lists. What am I missing?

# Discussion #8426: Getting Error while initiating DistributedWeightedRandomSampler
**Repository:** Project-MONAI/MONAI
**Author:** gssriram
**Created At:** 2025-04-22T19:35:50Z

## Description
Hi,

When I tried to initiate DistributedWeightedRandomSampler for my ImageDataset, I am getting this error:

```
File "/teamspace/studios/this_studio/luna25-baseline-public/train.py", line 257, in <module>
    train_sampler = DistributedWeightedRandomSampler(dataset=train_dataset, weights=sample_weights, num_samples_per_rank=2500, rank=0,
  File "/home/zeus/miniconda3/envs/cloudspace/lib/python3.10/site-packages/monai/data/samplers.py", line 100, in __init__
    super().__init__(dataset=dataset, even_divisible=even_divisible, num_replicas=num_replicas, rank=rank, **kwargs)
  File "/home/zeus/miniconda3/envs/cloudspace/lib/python3.10/site-packages/monai/data/samplers.py", line 52, in __init__
    super().__init__(dataset=dataset, num_replicas=num_replicas, rank=rank, shuffle=shuffle, **kwargs)
TypeError: DistributedSampler.__init__() got an unexpected keyword argument 'world_size'
```

My code is as follows:
```
train_dataset = ImageDataset(image_files=train_imgs, labels=train_labels, transform=train_transforms)
train_sampler = DistributedWeightedRandomSampler(dataset=train_dataset, weights=sample_weights, num_samples_per_rank=2500)
```

Can someone please help me with this.

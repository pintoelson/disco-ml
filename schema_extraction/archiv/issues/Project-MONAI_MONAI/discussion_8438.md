# Discussion #8438: Monai Supervised Trainer and Evaluator
**Repository:** Project-MONAI/MONAI
**Author:** CGTech242
**Created At:** 2025-05-06T03:08:27Z

## Description
Hello! Hope everyione is doing well. The model with the best metric is not saved. What could be the problem?

The following is my code.

`
import logging
import os
import sys
import tempfile
from glob import glob

import nibabel as nib
import numpy as np
import torch
from ignite.metrics import Accuracy

import monai
from monai.apps import get_logger
import monai.engines as me
import monai.transforms as mt
import monai.handlers as mh
import monai.inferers as mi
import monai.data as md

def main(data_dir):
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    get_logger("train_log")

    imagesTr = sorted(glob(os.path.join(data_dir, "imagesTr", "*.nii.gz")))
    labelsTr = sorted(glob(os.path.join(data_dir, "labelsTr", "*.nii.gz")))
    imagesTs = sorted(glob(os.path.join(data_dir, "imagesTs", "*.nii.gz")))

    split_idx = max(1, int(len(imagesTr) * 0.8))
    if split_idx >= len(imagesTr):  
        split_idx = len(imagesTr) - 1

    train_files = [{"image": img, "label": lbl} for img, lbl in zip(imagesTr[:split_idx], labelsTr[:split_idx])]
    val_files = [{"image": img, "label": lbl} for img, lbl in zip(imagesTr[split_idx:], labelsTr[split_idx:])]

    KEYS = ("image", "label")
    xforms = mt.Compose(
        [
            mt.LoadImageD(KEYS),
            mt.EnsureChannelFirstD("image"),
            mt.EnsureChannelFirstD("label", channel_dim="no_channel"),
            mt.OrientationD(KEYS, axcodes="RAS"),
            mt.SpacingD(KEYS, pixdim=(1.0, 1.0, 1.0), mode=("bilinear", "nearest")),
            mt.ScaleIntensityD(keys="image"),
            mt.ResizeD(KEYS, (64, 64, 32), mode=("trilinear", "nearest")),
            mt.RandAffineD(
                KEYS,
                spatial_size=(-1, -1, -1),
                rotate_range=(0, 0, np.pi / 2),
                scale_range=(0.1, 0.1),
                mode=("bilinear", "nearest"),
                prob=1.0,
            ),
        ]
    )

    val_xforms = mt.Compose(
        [
            mt.LoadImageD(KEYS),
            mt.EnsureChannelFirstD("image"),
            mt.EnsureChannelFirstD("label", channel_dim="no_channel"),
            mt.OrientationD(KEYS, axcodes="RAS"),
            mt.SpacingD(KEYS, pixdim=(1.0, 1.0, 1.0), mode=("bilinear", "nearest")),
            mt.ScaleIntensityD(keys="image"),
        ]
    )

    train_ds = md.CacheDataset(data=train_files, transform=xforms, cache_rate=0.5)
    train_loader = md.DataLoader(train_ds, batch_size=2, shuffle=True, num_workers=4)
    val_ds = md.CacheDataset(data=val_files, transform=val_xforms, cache_rate=1.0)
    val_loader = md.DataLoader(val_ds, batch_size=1, shuffle=False, num_workers=4)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    net = monai.networks.nets.UNet(
        spatial_dims=3,
        in_channels=2,
        out_channels=3,
        channels=(16, 32, 64, 128, 256),
        strides=(2, 2, 2, 2),
        num_res_units=2,
        norm=monai.networks.layers.Norm.BATCH,
    ).to(device)
    loss = monai.losses.DiceLoss(to_onehot_y=True, softmax=True)
    opt = torch.optim.Adam(net.parameters(), 1e-2)
    lr_scheduler = torch.optim.lr_scheduler.StepLR(opt, step_size=2, gamma=0.1)

    val_post_xforms = mt.Compose(
        [
            mt.EnsureTyped(keys="pred"),
            mt.Activationsd(keys="pred", softmax=True),
            mt.AsDiscreted(keys="pred", argmax=True),
            mt.KeepLargestConnectedComponentd(keys="pred", applied_labels=[1]),
        ]
    )

    val_handlers = [
        # apply “EarlyStop” logic based on the validation metrics
        mh.EarlyStopHandler(trainer=None, patience=2, score_function=lambda x: x.state.metrics["val_mean_dice"]),
        # use the logger "train_log" defined at the beginning of this program
        mh.StatsHandler(name="train_log", output_transform=lambda x: None),
        mh.TensorBoardStatsHandler(log_dir="./runs/", output_transform=lambda x: None),
        mh.TensorBoardImageHandler(
            log_dir="./runs/",
            batch_transform=mh.from_engine(["image", "label"]),
            output_transform=mh.from_engine(["pred"]),
        ),
        mh.CheckpointSaver(save_dir="./runs/", save_dict={"net": net}, save_key_metric=True),
    ]

    evaluator = me.SupervisedEvaluator(
        device=device,
        val_data_loader=val_loader,
        network=net,
        inferer=mi.SlidingWindowInferer(roi_size=(64, 64, 32), sw_batch_size=2, overlap=0.5),
        postprocessing=val_post_xforms,
        key_val_metric={
            "val_mean_dice": mh.MeanDice(include_background=True, output_transform=mh.from_engine(["pred", "label"]))
        },
        val_handlers=val_handlers,
        amp=True,
    )

    train_post_xforms = mt.Compose(
        [
            mt.Activationsd(keys="pred", softmax=True),
            mt.AsDiscreteD(keys=["pred", "label"], argmax=(True, False), to_onehot=3),
            mt.KeepLargestConnectedComponentd(keys="pred", applied_labels=[1]),
        ]
    )

    train_handlers = [
        # apply “EarlyStop” logic based on the loss value, use “-” negative value because smaller loss is better
        mh.EarlyStopHandler(
            trainer=None, patience=20, score_function=lambda x: -x.state.output[0]["loss"], epoch_level=False
        ),
        mh.LrScheduleHandler(lr_scheduler=lr_scheduler, print_lr=True),
        mh.ValidationHandler(validator=evaluator, interval=2, epoch_level=True),
        # use the logger "train_log" defined at the beginning of this program
        mh.StatsHandler(name="train_log", tag_name="train_loss", output_transform=mh.from_engine(["loss"], first=True)),
        mh.TensorBoardStatsHandler(
            log_dir="./runs/", tag_name="train_loss", output_transform=mh.from_engine(["loss"], first=True)
        ),
        mh.CheckpointSaver(save_dir="./runs/", save_dict={"net": net, "opt": opt}, save_interval=2, epoch_level=True),
    ]

    trainer = me.SupervisedTrainer(
        device=device,
        max_epochs=10,
        train_data_loader=train_loader,
        network=net,
        optimizer=opt,
        loss_function=loss,
        inferer=monai.inferers.SlidingWindowInferer((32, 32, -1), sw_batch_size=2),  # optionally using a sw inferer
        postprocessing=train_post_xforms,
        key_train_metric={
            "train_meandice": monai.handlers.MeanDice(output_transform=monai.handlers.from_engine(["pred", "label"]))
        },
        train_handlers=monai.handlers.StatsHandler(
            tag_name="train_loss", name="Training", output_transform=monai.handlers.from_engine(["loss"], first=True)
        ),
    )

    # set initialized trainer for "early stop" handlers
    val_handlers[0].set_trainer(trainer=trainer)
    train_handlers[0].set_trainer(trainer=trainer)
    trainer.run()

if __name__ == "__main__":
    data_dir = "/home/fersein/Documents/ProstateSegmentation/Task05_Prostate"
    main(data_dir)

`

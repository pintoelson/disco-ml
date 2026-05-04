# Discussion #8523: How to use DiceLoss for multiple-class 2D segmentation?
**Repository:** Project-MONAI/MONAI
**Author:** alexaex
**Created At:** 2025-07-29T13:32:35Z

## Description
Hi, I used monai DiceLoss to implement my segmentation task. However, the dice loss value is 0.8, while dice score is 0.7. This is weird. I think there must something be wrong.

So I wanna know how to use DiceLoss for multiple classes 2D segmentation task?
Though brats_segmentation_3d.ipynb from tutorial have mentioned how to do multiple-class segmentation, I didn't understand why it uses sigmoid instead of softmax in the DiceLoss. Does this sigmoid mean one pixel can belong to multiple classes?


The backbone will yield a tensor with shape [B, C, H, W], and the corresponding mask tensor with a shape [B, H, W].

I initialized MONAI DiceLoss, DiceMetric and trained my model with the following codes:
 ```
dice_loss = DiceLoss(include_background=True, to_onehot_y=True,
                                  sigmoid=False, softmax=True)
dice_metric = DiceMetric(include_background=True, num_classes=C)
def training_step(self, batch, batch_idx):
       # pytorch-lightning will do the backward propagation of the loss, here we just need to return a tensor.
       img, mask = batch
       logits = self.model(img)
       loss = dice_loss(logits, mask.unsqueeze(1))
       pred = logits.softmax(dim=1).argmax(dim=1)
       # convert BxHxW to BxCxHxW by monai.networks.one_hot
       pred = one_hot(pred[:, None, ...], dim=1, num_classes=C)
       gt = one_hot(mask[:, None, ...], dim=1, num_classes=C)
       dice_metric(pred, gt)
       return loss

## Comments
### Comment by NabJa at 2025-08-05T08:57:08Z
You are right. The `dice loss` should be `1 - dice score`. Consider this code that does fix some minor problems in your code:
```
batch_size, n_classes, h, w = 1, 3, 128, 128

dice_metric = DiceMetric(include_background=True, num_classes=n_classes, reduction="mean_batch")
dice_loss = DiceLoss(to_onehot_y=True, reduction="none")

# img = torch.rand(batch_size, n_classes, h, w)
mask = torch.randint(0, n_classes, size=(batch_size, 1, h, w))

logits = torch.rand(batch_size, n_classes, h, w) # self.model(img)
y_pred = torch.argmax(logits, dim=1, keepdim=True) # convert to label map

dice_score = dice_metric(y_pred, mask)
loss = dl(one_hot(y_pred, n_classes), mask).squeeze()

torch.allclose(dice_score, 1 - loss) # -> True
```

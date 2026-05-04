# Discussion #8464: Is the source code of UNETR module using different hidden status data compared to its original publication?
**Repository:** Project-MONAI/MONAI
**Author:** Y-SHI-MxLucid
**Created At:** 2025-05-29T10:33:58Z

## Description
I checked and found the source code of UNETR in monai.networks.nets be like this:
```python
class UNETR(nn.Module):
    ...
    def forward(self, x_in):
        x, hidden_states_out = self.vit(x_in)
        enc1 = self.encoder1(x_in)
        x2 = hidden_states_out[3]
        enc2 = self.encoder2(self.proj_feat(x2))
        x3 = hidden_states_out[6]
        enc3 = self.encoder3(self.proj_feat(x3))
        x4 = hidden_states_out[9]
        enc4 = self.encoder4(self.proj_feat(x4))
        dec4 = self.proj_feat(x)
        dec3 = self.decoder5(dec4, enc4)
        dec2 = self.decoder4(dec3, enc3)
        dec1 = self.decoder3(dec2, enc2)
        out = self.decoder2(dec1, enc1)
        return self.out(out)
```
and in ViT module source code:
```python
    def forward(self, x):
        x = self.patch_embedding(x)
        if hasattr(self, "cls_token"):
            cls_token = self.cls_token.expand(x.shape[0], -1, -1)
            x = torch.cat((cls_token, x), dim=1)
        hidden_states_out = []
        for blk in self.blocks:
            x = blk(x)
            hidden_states_out.append(x)
        x = self.norm(x)
        if hasattr(self, "classification_head"):
            x = self.classification_head(x[:, 0])
        return x, hidden_states_out
```
So, I guess the hidden_states_out[3], hidden_states_out[6], hidden_states_out[9] (and together with the normalized final output of entire ViT module) which were used in UNETR is basically the output of transformer block 4, 7, and 10? However, I found in the UNETR original publication that, UNETR indeed uses the output of 3rd, 6th 9th and 12th (the output of ViT) transformer block:

![image](https://github.com/user-attachments/assets/e179d1bb-b540-4ee6-ba62-de8616a7d714)

I guess it might be an indexing issue, so maybe you guys in developing team can have a check when possible?

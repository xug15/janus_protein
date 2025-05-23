import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
data = pd.read_csv("results/bigmodel_h512_l12_lr1e-5_metrics.csv")
val = data.dropna(subset = ['val_loss'])
train = data.dropna(subset = ['train_loss'])
epoch = train["epoch"]  
train_loss = train["train_loss"]
val_loss = val["val_loss"]
train_acc = train["train_acc"]
val_acc = val["val_acc"]

fig = plt.figure(figsize = (7,6)) 
p1 = pl.plot(epoch, train_loss,'r-', label = u'train_loss')
p2 = pl.plot(epoch,val_loss, 'b-', label = u'val_loss')
pl.legend()
pl.xlabel(u'Epoch')
pl.ylabel(u'MSE loss')
# ✅ 保存图片
plt.savefig("loss_curve.png", dpi=300, bbox_inches='tight')
plt.close()  # 可选：避免在某些IDE中自动弹窗

fig = plt.figure(figsize = (7,6)) 
p3 = pl.plot(epoch, train_acc,'r-', label = u'train_acc')
p4 = pl.plot(epoch,val_acc, 'b-', label = u'val_acc')
pl.legend()
pl.xlabel(u'Epoch')
pl.ylabel(u'PCC')
# ✅ 保存图片
plt.savefig("pcc_curve.png", dpi=300, bbox_inches='tight')
plt.close()  # 可选：避免在某些IDE中自动弹窗




import tensorflow as tf
import torchvision.transforms.functional as TF
from PIL import Image
import numpy as np
import yaml
import os

from src.tensortree import buildTree, rebuildImg

with open('./config.yml', 'r') as stream:
    meta = yaml.load(stream)

sdir = meta['crop']['dest']
mod = meta['crop']['mode']
rec = meta['crop']['recpath']
leafs = np.array([int(meta['split']['left']), int(meta['split']['middle']), int(meta['split']['right'])])
nimg = len([file for file in os.listdir(sdir) if os.path.isfile(os.path.join(sdir, file))]) // np.sum(leafs)

if not os.path.exists(rec):
      os.makedirs(rec)
else: print('path already exists')

patches = list()
seen = []
has = 0

def save(tensor, name):
    tf.keras.utils.save_img(rec+name+'.png', tensor, data_format="channels_first", file_format='png')

for file in sorted(os.listdir(sdir)):
    im = Image.open(sdir + '/' + file)
    im = TF.to_tensor(im)

    if str(os.path.splitext(os.path.basename(file))[0][0:3]) not in seen:
        seen.append(os.path.splitext(os.path.basename(file))[0][0:3])
    else:
        has+=1

    patches.append(im)

    if has==np.sum(leafs)-1:
        tree = buildTree(patches, leafs)
        reb = rebuildImg(tree, leafs)
        save(reb, str(os.path.splitext(os.path.basename(file))[0][0:3]))
        patches.clear()
        del tree
        has = 0

    
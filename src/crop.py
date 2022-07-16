import os
from PIL import Image
import torchvision.transforms.functional as TF
import numpy as np

def crop(dir, out, pat, edge=False):
    for file in os.listdir(dir):
        im = Image.open(dir + '/' + file)
        im = TF.to_tensor(im)
        imgheight=im.shape[1]
        imgwidth=im.shape[2]

        if edge:
            pass #recomposing from edge crop not fully implemented yet             
        else:
            sp = np.array([int(pat['split']['left']), int(pat['split']['middle']), int(pat['split']['right'])])
            div = 3
            if 0 in sp:
                index = np.nonzero(sp == 0)
                for i in index:
                    sp[i] = 99999
                    div -= 1
                ML = int(imgheight//sp[0])
                MM = int(imgheight//sp[1])
                MR = int(imgheight//sp[2])
                N = int(imgwidth//div)
            else:
                ML = int(imgheight//sp[0])
                MM = int(imgheight//sp[1])
                MR = int(imgheight//sp[2])
                N = int(imgwidth//div)
            
            vm = [ML, MM, MR]
            x=0
            for vi in vm:
                if vi == 0:
                    continue
                col_patch = im[:,:,x:x+N]
                for y in range(0, imgheight, vi):
                    row_patch = col_patch[:,y:y+vi,:]
                    if x == 0:
                        path = os.path.join(out, os.path.splitext(os.path.basename(file))[0] + '_L' + str(y//vi) + '.png')
                        patch = TF.to_pil_image(row_patch)
                        patch.save(path, 'PNG')
                    elif x == N and div == 3:
                        path = os.path.join(out, os.path.splitext(os.path.basename(file))[0] + '_M' + str(y//vi) + '.png')
                        patch = TF.to_pil_image(row_patch)
                        patch.save(path, 'PNG')
                    else:
                        path = os.path.join(out, os.path.splitext(os.path.basename(file))[0] + '_R' + str(y//vi) + '.png')
                        patch = TF.to_pil_image(row_patch)
                        patch.save(path, 'PNG')
                x+=N

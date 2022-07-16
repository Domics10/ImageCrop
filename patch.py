import src
from src.crop import crop
import yaml
import os

with open('./config.yml', 'r') as stream:
    PATHS = yaml.load(stream)

dir = PATHS['crop']['source']
out = PATHS['crop']['dest']
mode = PATHS['crop']['mode']

if not os.path.exists(out):
      os.makedirs(out)
else: assert not os.path.exists(out)

if mode == 'split':
    crop(dir, out, PATHS)
elif mode == 'edge':
    crop(dir, out, PATHS, True)
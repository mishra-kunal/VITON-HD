from PIL import Image
import os

# running the preprocessing

def resize_img(path):
    im = Image.open(path)
    im = im.resize((768, 1024))
    im.save(path)


for path in os.listdir('/content/inputs/test/cloth/'):
    resize_img(f'/content/inputs/test/cloth/{path}')

os.system("rm -rf /content/inputs/test/cloth/.ipynb_checkpoints")
os.system("python cloth-mask.py")    
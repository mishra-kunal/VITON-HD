from PIL import Image
import os
import shutil

# running the preprocessing

def resize_img(path):
    im = Image.open(path)
    im = im.resize((768, 1024))
    im.save(path)

for path in os.listdir('/content/VITON-HD/inputs/test/cloth/'):
    resize_img(f'/content/VITON-HD/inputs/test/cloth/{path}')

for path in os.listdir('/content/VITON-HD/inputs/test/image/'):
    resize_img(f'/content/VITON-HD/inputs/test/image/{path}')

os.system("rm -rf /content/VITON-HD/inputs/test/cloth/.ipynb_checkpoints")
os.system("python cloth-mask.py")
os.system("python Self-Correction-Human-Parsing/simple_extractor.py --dataset 'lip' --model-restore 'Self-Correction-Human-Parsing/checkpoints/final' --input-dir '/content/VITON-HD/inputs/test/image' --output-dir '/content/VITON-HD/inputs/test/image-parse'")
os.system(
    "cd openpose && ./build/examples/openpose/openpose.bin --image_dir /content/VITON-HD/inputs/test/image/ --write_json /content/VITON-HD/inputs/test/openpose-json/ --display 0 --render_pose 0 --hand")
os.system(
    "cd openpose && ./build/examples/openpose/openpose.bin --image_dir /content/VITON-HD/inputs/test/image/ --display 0 --write_images /content/VITON-HD/inputs/test/openpose-img/ --hand --render_pose 1 --disable_blending true")


# Move test folder to dataset folder
shutil.move('/content/VITON-HD/inputs/test', 'datasets/')

# Create test_pair.txt file
with open('/content/VITON-HD/datasets/test_pairs.txt', 'w') as file:
    image_files = os.listdir('/content/VITON-HD/datasets/test/image')
    cloth_files = os.listdir('/content/VITON-HD/datasets/test/cloth')

    # If there is one cloth and multiple images
    if len(cloth_files) == 1 and len(image_files) > 1:
        cloth = cloth_files[0]
        for image in image_files:
            file.write(f'{image} {cloth}\n')

    # If there is one image and multiple cloths
    elif len(image_files) == 1 and len(cloth_files) > 1:
        image = image_files[0]
        for cloth in cloth_files:
            file.write(f'{image} {cloth}\n')

    # If there is a one-to-one correspondence between image and cloth files
    else:
        for image, cloth in zip(image_files, cloth_files):
            file.write(f'{image} {cloth}\n')

os.chdir('/content/VITON-HD')
os.system("python test.py --name test")

os.system("rm -rf /content/VITON-HD/inputs")
os.system("rm -rf /content/VITON-HD/result/test/.ipynb_checkpoints")
os.system("rm -rf /content/VITON-HD/datasets/test")
os.system("rm -rf /content/VITON-HD/datasets/test_pairs.txt")
   
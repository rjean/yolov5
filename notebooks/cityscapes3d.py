# %%
#This notebooks allows converting cityscapes boundings boxes to Yolo.
dataset_dir = "/home/raphael/datasets/cityscapes"
annotations_dir = f"{dataset_dir}/gtBbox3d"
subset = "train"
import glob

categories = ["car","truck", "bus", "train", "motorcycle","bicycle"]

# %%
annotation_files = glob.glob(f"{annotations_dir}/{subset}/**/*.json",recursive=True)
# %%
import random
annotation_file = random.sample(annotation_files,1)[0]

# %%
import json
with open(annotation_file,"r") as f: 
    annotations = json.load(f)
annotations
# %%
import os
basename = os.path.basename(annotation_file)
basename

# %%
import re
def parse_basename(basename):
    m = re.match("(\w+)_(\d+)_(\d+)", basename)
    city = m[1]
    seq_num = m[2]
    frame_num = m[3]
    return city, seq_num, frame_num
city, seq_num, frame_num = parse_basename(basename)
city, seq_num, frame_num
# %%
from PIL import Image
from PIL import ImageDraw, ImageFont
def get_image_filename(city, seq_num, frame_num, subset="train"):
    image_file = f"{dataset_dir}/leftImg8bit/{subset}/{city}/{city}_{seq_num}_{frame_num}_leftImg8bit.png"
    return image_file
image_file = get_image_filename(city, seq_num, frame_num)
image = Image.open(image_file)
image

# %%
im_w, im_h = annotations["imgWidth"], annotations["imgHeight"]
im_w, im_h
# %%
for obj in annotations["objects"]:
    bbox = obj["2d"]["amodal"]
    label = obj["label"]
    draw = ImageDraw.Draw(image)
    x, y, w, h = bbox
    x1, y1 = x,y
    x2, y2 = x+w, y+h
    draw.rectangle([x1, y1, x2, y2])
    fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
    fnt2 = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 20)
    yolo_string = f"{categories.index(label)} {x/im_w} {y/im_h} {w/im_w} {h/im_h}"
    draw.text((x,y), label, font=fnt)
    draw.text((x,y+40), yolo_string, font=fnt2)
    
image
# %%
image.width, image.height

# %%
from tqdm import tqdm
subsets = ["train","val","test"]
for subset in subsets:
    image_files =  []
    annotation_files = glob.glob(f"{annotations_dir}/{subset}/**/*.json",recursive=True)
    for annotation_file in tqdm(annotation_files):
        with open(annotation_file,"r") as f: 
            annotations = json.load(f)
        basename = os.path.basename(annotation_file)
        city, seq_num, frame_num = parse_basename(basename)
        image_file = get_image_filename(city, seq_num, frame_num, subset)
        yolo_file = image_file.replace(".png",".txt")
        im_w, im_h = annotations["imgWidth"], annotations["imgHeight"]
        with open(yolo_file,"w") as f:
            for obj in annotations["objects"]:
                bbox = obj["2d"]["amodal"]
                label = obj["label"]
                x, y, w, h = bbox
                xc = x + w/2
                yc = y + h/2
                if label not in categories:
                    print(f"Ignoring label: {label} in {basename}")
                    continue
                yolo_line = f"{categories.index(label)} {xc/im_w} {yc/im_h} {w/im_w} {h/im_h}\n"
                f.write(yolo_line)
        image_files.append(image_file)
    with open(f"{dataset_dir}/{subset}.txt", "w") as f:
        for image_file in image_files:
            f.write(f"{image_file}\n")
        #f.writelines(image_files)
    #print(yolo_file)
    #break


# %%

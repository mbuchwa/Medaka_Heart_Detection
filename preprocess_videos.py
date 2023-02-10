import json
from natsort import natsorted
from PIL import Image
import argparse
import os
from utils.general import print_args
from pathlib import Path
import sys

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


def center_crop_images(image_dir, new_width_height=480):
    for video in os.listdir(ROOT / image_dir):
        video_path = image_dir + video + '/'
        video_dir = ROOT / video_path
        print(f'cropping video: {video}')
        for image in os.listdir(video_dir):
            if not os.path.isdir(image_dir + video):
                os.mkdir(image_dir + video)
            image_path = video_dir / image
            im = Image.open(image_path)
            width, height = im.size   # Get dimensions
            left = (width - new_width_height)/2
            top = (height - new_width_height)/2
            right = (width + new_width_height)/2
            bottom = (height + new_width_height)/2

            # Crop the center of the image
            im = im.crop((int(left), int(top), int(right), int(bottom)))
            im.save(image_dir + video + '/' + image)
        print(f'finished cropping video: {video} \n')


def convert_gt_points_to_yolo_format(label_dir, image_size=900., rescaled_size=480.):
    """It is assumed that the original uncropped image have a witdth and height of 900."""
    for filename in natsorted(os.listdir(ROOT / label_dir)):
        print(f'formatting {filename} label points to yolo format')
        file = os.path.join(ROOT / label_dir, filename)
        f = open(file, encoding='utf-8')
        data = json.load(f)
        #format of points is points = {'points' :[[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]]}
        x_center = data['points'][0][0] + 0.5*(data['points'][1][0] - data['points'][0][0]) #xmin + 0.5*(xmax - xmin)
        y_center = data['points'][0][1] + 0.5 * (data['points'][2][1] - data['points'][0][1])  # ymin + 0.5*(ymax - ymin)
        x_center = (x_center - (image_size - rescaled_size) / 2) / rescaled_size
        y_center = (y_center - (image_size - rescaled_size) / 2) / rescaled_size
        height = data['points'][2][1] - data['points'][0][1]  #ydiff
        width = data['points'][1][0] - data['points'][0][0] #xdiff
        height = height/rescaled_size
        width = width/rescaled_size

        line = "0 " + str(x_center) + " " + str(y_center) + " " + str(width) + " " + str(height)
        f.close()

        new_file = os.path.join(ROOT / label_dir, filename)
        txtFile = open(new_file.rstrip('.json') + ".txt", "w")
        txtFile.write(line)
        txtFile.close()
        print(f'finished formatting {filename} to yolo format \n')


def parse_opt():
    parser = argparse.ArgumentParser()

    parser.add_argument('--image_dir', type=str, default='data/test/images/',
                        help='directory of the .tif files to be cropped')
    parser.add_argument('--label_dir', type=str, default='data/test/labels/',
                        help='directory of the .json files with the label points which are converted to yolo format')
    opt = parser.parse_args()
    print_args(vars(opt))
    return opt


def main(opt):
    center_crop_images(opt.image_dir)
    if os.path.exists(opt.label_dir):
        convert_gt_points_to_yolo_format(opt.label_dir)


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)

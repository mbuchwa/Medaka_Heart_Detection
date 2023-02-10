import os
from PIL import Image
import numpy as np

images_dir = '/home/ben/PycharmProjects/pythonProject/yolov5/FishYolo/cropped_480/images/'
new_width = 480
new_height = 480

for video in sorted(os.listdir(images_dir)):
    video_dir = images_dir + video + '/'
    image_path = video_dir + os.listdir(video_dir)[0]
    im = Image.open(image_path)
    im = np.asarray(im, dtype="int32")
    print(video_dir, im.sum(), np.max(im)-np.min(im))



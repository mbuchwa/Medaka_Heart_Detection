import os
from PIL import Image
import cv2

images_dir = '/home/ben/PycharmProjects/pythonProject/yolov5/FishYolo/cropped_480/images/'
new_images_dir = '/home/ben/PycharmProjects/pythonProject/yolov5/FishYolo/images_480_contrast/'

for video in os.listdir(images_dir):
    video_dir = images_dir + video + '/'
    print(f'process video: {video}')
    for image in os.listdir(video_dir):
        if not os.path.isdir(new_images_dir + video):
            os.makedirs(new_images_dir + video)
        image_path = video_dir + image
        im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        im = clahe.apply(im)
        cv2.imwrite(new_images_dir + video + '/' + image, im)
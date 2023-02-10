import os
from PIL import Image

images_dir = '/home/ben/PycharmProjects/pythonProject/yolov5/FishYolo/images_old/'
new_images_dir = '/home/ben/PycharmProjects/pythonProject/yolov5/FishYolo/images_cropped_480/'
new_width = 480
new_height = 480

for video in os.listdir(images_dir):
    video_dir = images_dir + video + '/'
    print(f'process video: {video}')
    for image in os.listdir(video_dir):
        if not os.path.isdir(new_images_dir + video):
            os.makedirs(new_images_dir + video)
        image_path = video_dir + image
        im = Image.open(image_path)
        width, height = im.size   # Get dimensions
        left = (width - new_width)/2
        top = (height - new_height)/2
        right = (width + new_width)/2
        bottom = (height + new_height)/2

        # Crop the center of the image
        im = im.crop((int(left), int(top), int(right), int(bottom)))

        im.save(new_images_dir + video + '/' + image)
#Author: Ben Dangelmayr
#Short script to extract rectangular, non-quadratic bounding box out of a polygon given by json points
import json
import os
from natsort import natsorted
import chardet

directory = '/home/ben/PycharmProjects/pythonProject/Labels'
new_directory = '/home/ben/PycharmProjects/pythonProject/yolov5/FishYolo/labels_cropped_480_2'
for filename in natsorted(os.listdir(directory)):
    # if not os.path.isdir(new_directory + filename):
    #     os.makedirs(new_directory)
    file = os.path.join(directory, filename)
    f = open(file)
    data = json.load(f)
    points = []
    #format of points is points = {'points' :[[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]]}
    x_center = data['points'][0][0] + 0.5*(data['points'][1][0] - data['points'][0][0]) #xmin + 0.5*(xmax - xmin)
    y_center = data['points'][0][1] + 0.5 * (data['points'][2][1] - data['points'][0][1])  # ymin + 0.5*(ymax - ymin)
    x_center = (x_center - (900 - 480) / 2) / 480
    y_center = (y_center - (900 - 480) / 2) / 480
    height = data['points'][2][1] - data['points'][0][1]  #ydiff
    width = data['points'][1][0] - data['points'][0][0] #xdiff
    height = height/480.
    width = width/480.

    line = "0 " + str(x_center) + " " + str(y_center) + " " + str(width) + " " + str(height)
    f.close()

    new_file = os.path.join(new_directory, filename)
    txtFile = open(new_file + ".txt", "w")
    txtFile.write(line)
    txtFile.close()
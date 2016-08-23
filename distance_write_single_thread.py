from skimage.feature import canny
from skimage import img_as_ubyte
import glob
import cv2
import os
import re

canny_sigma = 2.25


def _find_bottom_edge(img_bw):
    for i in reversed(xrange(len(img_bw))):
        for j in xrange(len(img_bw[0])):
            if(img_bw[i][j] > 0):
                point = (j, i)
                return point


fh = open("distances_sigma_" + str(canny_sigma) + ".txt", "a")
files = glob.glob(os.getcwd() + "/resize150/*")

for input_file_path in files:
    int_values = []
    path_sections = input_file_path.split("/")

    for string in path_sections:
        if re.search(r'\d+', string) is not None:
            int_values.append(int(re.search(r'\d+', string).group()))

    file_count = int_values[-1]
    print file_count

    image = cv2.imread(input_file_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    edges = img_as_ubyte(canny(image, sigma=canny_sigma))
    img_bw = cv2.threshold(edges, 250, 255, cv2.THRESH_BINARY)[1]

    point = _find_bottom_edge(img_bw)
    distance = len(img_bw) - point[1]

    output = str(file_count) + ":" + str(distance) + "\n"
    fh.write(output)
    fh.flush()

fh.close()

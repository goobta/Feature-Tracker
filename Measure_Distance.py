import cv2
import numpy as np
import os
import glob
import matplotlib.pyplot as plot
import re
import multiprocessing
from skimage.feature import canny
from skimage import img_as_ubyte


def create_figure(path):
    figure = plot.figure("Crash Labeller")
    image_raw = figure.add_subplot(221)
    image_edges = figure.add_subplot(222)
    text = figure.add_subplot(223)
    text_ax = text.axis([-1, 1, -1, 1])

    int_values = []
    path_sections = path.split("/")

    for string in path_sections:
        if re.search(r'\d+', string) is not None:
            int_values.append(int(re.search(r'\d+', string).group()))

    file_count = int_values[-1]
    crash = False

    print file_count

    image = cv2.imread(path)

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = img_as_ubyte(canny(img_gray, sigma=canny_sigma))
    img_bw = cv2.threshold(edges, 250, 255, cv2.THRESH_BINARY)[1]

    point = find_bottom_edge(img_bw)
    distance = np.sqrt(np.power(point[0] - len(img_bw[0]) / 2, 2) + np.power(point[1] - len(img_bw), 2))

    cv2.line(image, point, (len(img_bw[0]) / 2, len(img_bw)), (0, 255, 0), 1)

    if distance <= _threshold:
        crash = True

    image_raw.imshow(image)
    image_raw.set_title("Image raw")
    image_edges.imshow(edges)
    image_edges.set_title("Edges")
    crash_status = text.text(-0.5, 0.5, "Crash Status: " + str(crash))
    distance_status = text.text(-0.5, -0.5, "Distance: " + str(distance))

    figure.savefig("figures_sigma_" + str(canny_sigma) + "/FRAME_" + str(file_count))
    crash_status.remove()
    distance_status.remove()

def find_bottom_edge(img_bw):
    for i in reversed(xrange(len(img_bw))):
        for j in xrange(len(img_bw[0])):
            if(img_bw[i][j] > 0):
                point = (j, i)
                return point

_threshold = 30
canny_sigma = 2.5
threads = 6

plot.ion()
os.mkdir(os.getcwd() + "/figures_sigma_" + str(canny_sigma))
files = glob.glob("/home/agupta/Documents/Projects/Feature-Tracker/bw150/*")

print files

pool = multiprocessing.Pool(threads)
pool.map(create_figure, files)

#create_figure(files)
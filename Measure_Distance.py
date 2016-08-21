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
    try:
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
        distance = len(img_bw) - point[1]

        cv2.line(image, point, (len(img_bw[0]) / 2, len(img_bw)), (0, 255, 0), 1)

        if distance <= _threshold:
            crash = True

        image_raw.imshow(image)
        image_raw.set_title("Image raw")
        image_edges.imshow(edges)
        image_edges.set_title("Edges")
        crash_status = text.text(-0.5, 0.5, "Crash Status: " + str(crash))
        distance_status = text.text(-0.5, -0.5, "Distance: " + str(distance))

        figure.savefig("sigma_" + str(canny_sigma) + "_thresh_" + str(_threshold) + "/FRAME_" + str(file_count))
        crash_status.remove()
        distance_status.remove()

    except Exception:
        print "Error with file"

def find_bottom_edge(img_bw):
    for i in reversed(xrange(len(img_bw))):
        for j in xrange(len(img_bw[0])):
            if(img_bw[i][j] > 0):
                point = (j, i)
                return point

_threshold = 30
canny_sigma = 2.25
threads = 8

plot.ion()
os.mkdir(os.getcwd() + "/sigma_" + str(canny_sigma) + "_thresh_" + str(_threshold))
files = glob.glob(os.getcwd() + "/resize150/*")

pool = multiprocessing.Pool(threads)
pool.map(create_figure, files)

#create_figure(files)
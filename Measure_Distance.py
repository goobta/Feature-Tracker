import cv2
import numpy as np
import os
import glob
from skimage.feature import canny
from skimage import img_as_ubyte

def find_bottom_edge(img_bw):
    for i in reversed(xrange(len(img_bw))):
        for j in xrange(len(img_bw[0])):
            print i, j, img_bw[i][j]

            if(img_bw[i][j] > 0):
                point = (j, i)
                print point

                return point

files = glob.glob(os.getcwd() + "/bw150/*")

for path in files:
    image = cv2.imread(path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    edges = img_as_ubyte(canny(image, sigma=3))
    img_bw = cv2.threshold(edges, 250, 255, cv2.THRESH_BINARY)[1]

    point = find_bottom_edge(img_bw)

    cv2.line(img_bw, point, (len(img_bw[0]) / 2, len(img_bw)), 255, 1)

    cv2.imshow("Image", image)
    cv2.imshow("Edges", img_bw)
    cv2.waitKey(0)
import cv2
import numpy as np
import os
import glob
from skimage.feature import canny
from skimage import img_as_ubyte

files = glob.glob(os.getcwd() + "/bw150/*")

for path in files:
    image = cv2.imread(path)
    edges = img_as_ubyte(canny(image, sigma=2))

    cv2.imshow("Edges", edges)
    cv2.waitKey(0)
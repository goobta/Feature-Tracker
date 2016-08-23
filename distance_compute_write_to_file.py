from skimage.feature import canny
from skimage import img_as_ubyte
import multiprocessing
import glob
import cv2
import re

def worker(input_file, queue):


def main():
    manager = multiprocessing.Manager()
    queue = manager.Queue()


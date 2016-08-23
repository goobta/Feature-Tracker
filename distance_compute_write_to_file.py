from skimage.feature import canny
from skimage import img_as_ubyte
import multiprocessing
import glob
import cv2
import re

canny_sigma = 2.25
workers = 80

def _find_bottom_edge(img_bw):
    for i in reversed(xrange(len(img_bw))):
        for j in xrange(len(img_bw[0])):
            if(img_bw[i][j] > 0):
                point = (j, i)
                return point

def worker(input_file_path, queue):
    int_values = []
    path_sections = input_file_path.split("/")

    for string in path_sections:
        if re.search(r'\d+', string) is not None:
            int_values.append(int(re.search(r'\d+', string).group()))

    file_count = int_values[-1]

    image = cv2.imread(input_file_path)

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = img_as_ubyte(canny(img_gray, sigma=canny_sigma))
    img_bw = cv2.threshold(edges, 250, 255, cv2.THRESH_BINARY)[1]

    point = _find_bottom_edge(img_bw)
    distance = len(img_bw) - point[1]

    output = str(file_count) + ":" + str(distance) + "\n"
    queue.put(output)

    return output

def listener(queue):
    fh = open("distances_sigma_" + str(canny_sigma) + ".txt")

    while True:
        queue_value = queue.get()

        if(queue_value == "kill"):
            print "Listener Killed"
            break

        fh.write(queue_value)
        fh.flush()
    fh.close()

def main():
    manager = multiprocessing.Manager()
    queue = manager.Queue()


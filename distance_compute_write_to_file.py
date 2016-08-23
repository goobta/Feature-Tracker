from skimage.feature import canny
from skimage import img_as_ubyte
import multiprocessing
import glob
import cv2
import os
import re

canny_sigma = 2.25
workers = 60


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

    image = cv2.imread(input_file_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    edges = img_as_ubyte(canny(image, sigma=canny_sigma))
    img_bw = cv2.threshold(edges, 250, 255, cv2.THRESH_BINARY)[1]

    point = _find_bottom_edge(img_bw)
    distance = len(img_bw) - point[1]

    output = str(file_count) + ":" + str(distance) + "\n"
    queue.put(output)

    return output


def listener(queue):
    fh = open("distances_sigma_" + str(canny_sigma) + ".txt", "a")

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
    pool = multiprocessing.Pool(multiprocessing.cpu_count() + 2)

    files = glob.glob(os.getcwd() + "/resize150/*")
    watcher = pool.apply_async(listener, (queue,))

    jobs = []
    for i in xrange(len(files)):
        job = pool.apply_async(worker, (files[i], queue))
        jobs.append(job)

    for job in jobs:
        job.get()

    queue.put("Kill")
    pool.close()

if __name__ == "__main__":
    main()
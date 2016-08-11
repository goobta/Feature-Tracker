import cv2
import numpy as np

IMAGE_FILENAME = "car_test.jpg"

image = cv2.imread(IMAGE_FILENAME)
image_numpy = np.array(image)

r_max = []
g_max = []
b_max = []

r_min = []
g_min = []
b_min = []

for i in image_numpy:
    b_max.append(i.max(axis=0)[0])
    g_max.append(i.max(axis=0)[1])
    r_max.append(i.max(axis=0)[2])

    b_min.append(i.min(axis=0)[0])
    g_min.append(i.min(axis=0)[1])
    r_min.append(i.min(axis=0)[2])

print "Max R: " + str(np.amax(r_max))
print "Max G: " + str(np.amax(g_max))
print "Max B: " + str(np.amax(b_max))

print "Min R: " + str(np.amin(r_min))
print "Min G: " + str(np.amin(g_min))
print "Min B: " + str(np.amin(b_min))

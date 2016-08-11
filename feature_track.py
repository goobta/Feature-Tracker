import numpy as np
import cv2
import matplotlib

capture = cv2.VideoCapture("feature_tracking_test.mp4")

#while True:
succ, image = capture.read()

#image = cv2.imread("test.jpg")

#if succ:
lower = np.array([86, 31, 4])
upper = np.array([255, 100, 100])
mask = cv2.inRange(image, lower, upper)

cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
c = max(cnts, key=cv2.contourArea)

peri = cv2.arcLength(c, True)
approx = cv2.approxPolyDP(c, 0.05 * peri, True)

cv2.drawContours(image, [approx], -1, (255, 0, 255), 4)
cv2.imshow("Image", image)
cv2.waitKey(0)
#else:
    # break
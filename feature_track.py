import numpy as np
import cv2
import matplotlib


# def track_features(video_input):
#     capture = cv2.VideoCapture(video_input)
#

def extract_roi(poly):
    poly_numpy = np.array(poly).squeeze()

    x_start = poly_numpy.min(axis=0)[0]
    y_start = poly_numpy.min(axis=0)[1]
    x_end = poly_numpy.max(axis=0)[0]
    y_end = poly_numpy.max(axis=0)[1]

    return x_start, y_start, x_end, y_end

capture = cv2.VideoCapture("feature_tracking_test.mp4")

lower = np.array([200, 200, 200])
upper = np.array([255, 255, 255])

previous_location = None

while True:
    succ, image = capture.read()

    if succ:
        mask = cv2.inRange(image, lower, upper)

        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        feature = max(contours, key=cv2.contourArea)

        perimeter = cv2.arcLength(feature, True)
        approximate_region = cv2.approxPolyDP(feature, 0.05 * perimeter, True)

        xs, ys, xe, ye = extract_roi(approximate_region)

        cv2.rectangle(image, (xs, ys), (xe, ye), 255, 2)

        if previous_location is not None:
            cv2.line(image, ((xs + xe) / 2, (ys + ye) / 2), previous_location, (255, 255, 0), thickness=3, lineType=8)
            previous_location = ((xs + xe) / 2, (ys + ye) / 2)
        else:
            previous_location = ((xs + xe) / 2, (ys + ye) / 2)

        print previous_location

        cv2.imshow("Image", image)
        cv2.waitKey(0)

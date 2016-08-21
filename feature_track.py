import numpy as np
import cv2



def track_features(video_input):
    feature_definitions = {
        "car": [(40, 150, 100), (120, 255, 170), (), ()],
        "front_bumper": [(70, 65, 55), (100, 80, 80), 0.001, ()],
        # "back_bumper": [(), (), 0.0416, ()],
        "right_side": [(75, 75, 85), (100, 110, 115), 0.003, ()]
        # "left_side": [(), (), 0.03846, ()]
    }

    CAR_FRAME_PADDING = 50

    capture = cv2.VideoCapture(video_input)

    while True:
        succ, image = capture.read()

        if succ:
            image_denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
            cc_delta = brightness_delta(image_denoised)

            print tuple(np.add(feature_definitions["car"][0], cc_delta))

            car_mask = cv2.inRange(image_denoised, tuple(np.add(feature_definitions["car"][0], cc_delta)), tuple(np.add(feature_definitions["car"][1], cc_delta)))
            car_contours, _ = cv2.findContours(car_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            car = max(car_contours, key=cv2.contourArea)
            car_perimeter = cv2.arcLength(car, True)
            approximate_region = cv2.approxPolyDP(car, 0.05 * car_perimeter, True)

            car_x_start, car_y_start, car_x_end, car_y_end = extract_roi(approximate_region)
            max_y, max_x, channels = image_denoised.shape

            if car_x_start - CAR_FRAME_PADDING >= 0:
                car_x_start -= CAR_FRAME_PADDING
            else:
                car_x_start = 0

            if car_y_start - CAR_FRAME_PADDING >= 0:
                car_y_start -= CAR_FRAME_PADDING
            else:
                car_y_start = 0

            if car_x_end + CAR_FRAME_PADDING <= max_x:
                car_x_end += CAR_FRAME_PADDING
            else:
                car_x_end = max_x

            if car_y_end + CAR_FRAME_PADDING <= max_y:
                car_y_end += CAR_FRAME_PADDING
            else:
                car_y_end = max_y

            car_frame = image_denoised[car_y_start:car_y_end, car_x_start:car_x_end]
            car_area = (car_x_end - car_x_start) * (car_y_end - car_y_start)

            cv2.rectangle(image_denoised, (car_x_start, car_y_start), (car_x_end, car_y_end), (0, 255, 255), 1)

            for key, values in feature_definitions.iteritems():
                if key == "car":
                    continue
                else:
                    feature_definition = feature_definitions[key]

                    feature_mask = cv2.inRange(car_frame, tuple(np.add(feature_definition[0], cc_delta)), tuple(np.add(feature_definition[1], cc_delta)))
                    feature_contours, _ = cv2.findContours(feature_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    if len(feature_contours) > 0:
                        feature = max(feature_contours, key=cv2.contourArea)
                        feature_perimeter = cv2.arcLength(feature, True)
                        feature_approx = cv2.approxPolyDP(feature, 0.05 * feature_perimeter, True)

                        x_start, y_start, x_end, y_end = extract_roi(feature_approx)
                        feature_area = (x_end - x_start) * (y_end - y_start)

                        if feature_area >= (car_area * feature_definition[2]):
                            if feature_definition[3] == ():
                                cv2.rectangle(image_denoised, (x_start + car_x_start, y_start + car_y_start), (x_end + car_x_start, y_end + car_y_start), (0, 255, 0), 1)

                                feature_definition[3] = (car_x_start + (x_start + x_end) / 2, car_y_start + (y_start + y_end) / 2)
                            else:
                                cv2.rectangle(image_denoised, (x_start + car_x_start, y_start + car_y_start), (x_end + car_x_start, y_end + car_y_start), (0, 255, 0), 1)
                                cv2.line(image_denoised, (car_x_start + (x_start + x_end) / 2, car_y_start + (y_start + y_end) / 2), feature_definition[3], (255, 255, 0), 1)

                                feature_definition[3] = (car_x_start + (x_start + x_end) / 2, car_y_start + (y_start + y_end) / 2)
                        else:
                            feature_definition[3] = ()
                    else:
                        feature_definition[3] = ()

            cv2.imshow("Mask", car_mask)
            cv2.imshow("denoised", image_denoised)
            cv2.imshow("Frame", image)
            cv2.imshow("Car Frame", car_frame)

            cv2.waitKey(0)
        else:
            break

def extract_roi(poly):
    poly_numpy = np.array(poly).squeeze()

    x_start = poly_numpy.min(axis=0)[0]
    y_start = poly_numpy.min(axis=0)[1]
    x_end = poly_numpy.max(axis=0)[0]
    y_end = poly_numpy.max(axis=0)[1]

    return x_start, y_start, x_end, y_end

def brightness_delta(input_image):
    SAMPLE_FRAME_SIZE = 400
    BASELINE_AVERAGE = 135.1991

    image_bw = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    height, length = image_bw.shape

    sample_frame = image_bw[(height / 2) - SAMPLE_FRAME_SIZE / 2:(height / 2) + SAMPLE_FRAME_SIZE / 2, (length / 2) - SAMPLE_FRAME_SIZE / 2:(length/ 2) + SAMPLE_FRAME_SIZE / 2]
    color_average = np.average(np.array(sample_frame).squeeze())

    print color_average
    print color_average - BASELINE_AVERAGE

    return color_average - BASELINE_AVERAGE

# capture = cv2.VideoCapture("feature_tracking_test.mp4")
#
# lower = np.array([70, 20, 1])
# upper = np.array([255, 80, 110])
#
# previous_location = None
#
# while True:
#     # succ, image = capture.read()
#
#     succ = True
#     image = cv2.imread("car_blurred.jpg")
#
#     if succ:
#         mask = cv2.inRange(image, lower, upper)
#
#         cv2.imshow("mask", mask)
#         cv2.waitKey(0)
#
#         contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         feature = max(contours, key=cv2.contourArea)
#
#         perimeter = cv2.arcLength(feature, True)
#         approximate_region = cv2.approxPolyDP(feature, 0.05 * perimeter, True)
#
#         print len(approximate_region)
#
#         xs, ys, xe, ye = extract_roi(approximate_region)
#
#         cv2.drawContours(image, [approximate_region], -1, (0, 255, 255), 4)
#         cv2.rectangle(image, (xs, ys), (xe, ye), 255, 2)
#
#         if previous_location is not None:
#             cv2.line(image, ((xs + xe) / 2, (ys + ye) / 2), previous_location, (255, 255, 0), thickness=3, lineType=8)
#             previous_location = ((xs + xe) / 2, (ys + ye) / 2)
#         else:
#             previous_location = ((xs + xe) / 2, (ys + ye) / 2)
#
#         cv2.imshow("Image", image)
#         cv2.waitKey(0)

track_features("4.mp4")

from sys import maxsize
import cv2
import numpy as np
from time import perf_counter
import threading
#from ball_blender import Blender

np.random.seed(0)


class Detector:
    def __init__(self, video_path, config_path, model_path, classes_path, ui_object):
    #def __init__(self, video_path, config_path, model_path, classes_path):
        self.video_path = video_path
        self.config_path = config_path
        self.model_path = model_path
        self.classes_path = classes_path
        self.running = False
        self.ui_object = ui_object

        # Setup network model
        self.network = cv2.dnn_DetectionModel(self.model_path, self.config_path)
        self.network.setInputSize(320, 320)
        self.network.setInputScale(1.0 / 127.5)
        self.network.setInputMean((127.5, 127.5, 127.5))
        self.network.setInputSwapRB(True)

        self.readClasses()
        
        self.is_calibrating = False
        self.is_driving = False

        self.calibrated_x = None
        self.calibrated_y = None

        self.correctly_calibrated = False

        # Tracked object properties
        self.relative_distance = None
        self.relative_angle = None # Right is positive angle, left is negative angle
        self.object_bbx = None

    def readClasses(self):
        with open(self.classes_path, "r") as file:
            self.classes_list = file.read().splitlines()

        # The model predicts index 0 as background, so manually insert this
        self.classes_list.insert(0, "__Background__")

        # Get random integer BGR colours for each class label
        self.colour_list = np.random.uniform(low=0, high=255, size=(len(self.classes_list), 3))
        self.colour_list = [tuple(map(int, colour)) for colour in self.colour_list]

    def offVideo(self):
        self.running = False
        cv2.destroyAllWindows()

    def onVideo(self, tracked_obj: str=None):
        capture = cv2.VideoCapture(self.video_path)

        if not capture.isOpened():
            print("Error accessing video, terminating...")
            return

        successful, image = capture.read()

        # Keep looping through frames while the frames are successfully loaded
        start = perf_counter()
        self.running = True
        self.number = 0
        while successful and self.running:
            # Calculate FPS
            end = perf_counter()
            fps = 1 / (end - start)
            start = end

            # Detect objects in current frame with certainty of 50% or above
            class_label_ids, confidences, bounding_boxes = self.network.detect(image, confThreshold=0.5)

            # Change bounding boxes and confidences to lists
            bounding_boxes = list(bounding_boxes)
            confidences = list(np.array(confidences).reshape(1, -1)[0])
            confidences = list(map(float, confidences))  # Changes confidences to floats

            # Eliminate bounding boxes with an overlap. This returns indexes of bounding boxes with overlap below certain threshold.
            bounding_boxes_ids = cv2.dnn.NMSBoxes(bounding_boxes, confidences, score_threshold=0.5, nms_threshold=maxsize)

            if len(bounding_boxes_ids) != 0:
                # Loop through valid boxes
                for i in range(0, len(bounding_boxes_ids)):
                    idx = np.squeeze(bounding_boxes_ids[i])
                    curr_box = bounding_boxes[idx]
                    curr_confidence = confidences[idx]
                    curr_label_idx = np.squeeze(class_label_ids[idx])

                    curr_label = self.classes_list[curr_label_idx]
                    curr_colour = self.colour_list[curr_label_idx]

                    # Get box info
                    x, y, w, h = curr_box

                    # Draw box
                    cv2.rectangle(image, (x, y), (x + w, y + h), color=curr_colour, thickness=1)

                    # Draw text
                    cv2.putText(image, f"{curr_label}: {curr_confidence:.3f}", (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.4, curr_colour)

                    # Print out bbx for wanted 
                    if tracked_obj:
                        if curr_label == tracked_obj:
                            if self.is_calibrating:
                                self.calibrated_x = image.shape[1]
                                self.calibrated_y = image.shape[0]
                                self.correctly_calibrated = True
                                print("Calibration successful! You may drive.")
                                self.is_calibrating = False
                            
                            elif self.is_driving and self.correctly_calibrated:
                                image_width = image.shape[1]
                                image_height = image.shape[0]
                                #Assuming FOV is 60 (maybe a parameter should be added)
                                field_of_view = 60
                                direction_angle = field_of_view*((x+(w/2))/image_width)-(field_of_view/2)
                                self.relative_angle = direction_angle

                                self.relative_distance = ((self.calibrated_x/image_width)+(self.calibrated_y/image_height))/2


            # Draw FPS
            cv2.putText(image, f"FPS: {fps:.1f}", (20, 20), cv2.FONT_HERSHEY_DUPLEX, 0.4, (0, 0, 255), 1)
            # Show the object bounding boxes on the image
            #cv2.imshow("Result", cv2.resize(image, (1600, 900)))
            cv2.imwrite("video" + str(self.number) + ".png", cv2.resize(image, (1600, 900)))
            print("pp")
            #self.ui_object.worker.RerenderCommand(self.number)
            self.ui_object.rerender = True
            self.ui_object.render_number = self.number
            self.number += 1
            self.number = self.number % 2

            # Quit loop functionality
            # The & 0xFF is used to take the last byte of the key press since numlock can sometimes change the first byte of a key press. 
            # 0xFF just represents 11111111 (8 1s).
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == ord("c") or key == ord("Q") or key == ord("C"):
                break

            # Get next frame
            successful, image = capture.read()

        # Destroy all cv2 windows when video stream breaks
        cv2.destroyAllWindows()

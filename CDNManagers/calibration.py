from time import sleep
from CDNManagers.car_control import CarControl
from CDNManagers.detector import Detector


# Template class for the calibration of the car on initialisation
# Add code to perform preliminary checks like cameras working etc

class Calibrate:
    def start_calibration(self, controller, detector):

        print("Attempting to establish Arduino connection")
        controller.ControlSetup()
        sleep(1)
        print("Starting calibration in 3, DO NOT move calibration object in frame.")
        sleep(1)
        print("Starting calibration in 2, DO NOT move calibration object in frame.")
        sleep(1)
        print("Starting calibration in 1, DO NOT move calibration object in frame.")
        sleep(1)
        print("Starting calibration. If you move the calibration object then you are stinky! (ಠ~ಠ)")
        detector.is_calibrating = True
        print("Computer vision initialising now.")
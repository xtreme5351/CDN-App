import os
from PyQt5.QtWidgets import *
from CDNManagers import Detector
from CDNManagers import Calibrate
from CDNManagers import Connect
from CDNManagers import CV


def resolve_files(debug=False) -> tuple:
    vid_path = 0
    if not debug:
        config_path = os.path.abspath("CDNManagers\data\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
        model_path = os.path.abspath("CDNManagers\data\\frozen_inference_graph.pb")
        # the above absolutely shits itself
        #  Use debug path for now
        classes_path = os.path.abspath("CDNManagers\data\coco.names")
        print(config_path, model_path, classes_path)
    else:
        print("L tbh, using debug path")
        # config_path = "/Users/pc/PycharmProjects/cdn_app/CDNManagers/data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        config_path = "/Users/pc/PycharmProjects/cdn_app/CDNManagers/data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        model_path = "/Users/pc/PycharmProjects/cdn_app/CDNManagers/data/frozen_inference_graph.pb"
        # the above poos when this = os.path.join is used
        #  Hard coded for now, just to make sure it works
        classes_path = "/Users/pc/PycharmProjects/cdn_app/CDNManagers/data/coco.names"
    return vid_path, config_path, model_path, classes_path


class CDNApp(QWidget):
    def __init__(self, parent=None):
        if parent is not None:
            super(QWidget, self).__init__(parent)
        else:
            super().__init__()
        # Widgets to be used
        self.calibrate = QPushButton("Start calibration")
        self.start = QPushButton("Start driving")
        self.conn = QPushButton("Connect to car")
        self.stop = QPushButton("Stop driving")
        # Bools
        self.has_conn = False
        self.has_calibrated = False
        self.has_started = True
        # Managers
        self.connectionManager = Connect()
        self.calibrationManager = Calibrate()
        self.detector = Detector(*resolve_files())
        self.cv = CV(self.detector)
        self.initUI()

    def setButtons(self):
        self.conn.clicked.connect(self.onConnect)
        self.calibrate.clicked.connect(self.onCalibrate)
        self.start.clicked.connect(self.onStart)
        self.stop.clicked.connect(self.onStop)
        self.calibrate.setEnabled(self.has_conn)
        self.start.setEnabled(self.has_calibrated)
        self.stop.setEnabled(self.has_started)

    def initUI(self):
        self.setButtons()

        layout = QVBoxLayout()
        layout.addWidget(self.conn)
        layout.addWidget(self.calibrate)
        layout.addWidget(self.start)
        layout.addWidget(self.stop)

        self.setGeometry(200, 200, 300, 150)
        self.setLayout(layout)
        self.setWindowTitle('CDN Controller')
        self.show()

    def onCalibrate(self):
        self.has_calibrated = True
        self.start.setEnabled(self.has_calibrated)
        self.calibrationManager.start_calibration()

    def onStart(self):
        print("Starting")
        self.has_started = True
        self.cv.start()

    def onStop(self):
        print("Stopping")
        self.has_started = False
        self.cv.stop()

    def onConnect(self):
        self.has_conn = True
        self.calibrate.setEnabled(self.has_conn)
        self.connectionManager.start_connection()

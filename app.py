import os
from PyQt5.QtWidgets import *
from CDNManagers import Detector
from CDNManagers import Calibrate
from CDNManagers import Connect
from CDNManagers import CV
from CDNManagers import CarControl


def resolve_files() -> tuple:
    vid_path = 0
    config_path = os.path.abspath("CDNManagers/data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    model_path = os.path.abspath("CDNManagers/data/frozen_inference_graph.pb")
    classes_path = os.path.abspath("CDNManagers/data/coco.names")
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
        self.reset = QPushButton("Reset")
        # Bools
        self.has_conn = False
        self.has_calibrated = False
        self.has_started = False
        # Managers
        self.connectionManager = Connect()
        self.calibrationManager = Calibrate()
        self.detector = Detector(*resolve_files())
        self.cv = CV(self.detector, "stop sign")
        self.controller = CarControl(self.detector)
        self.initUI()

    def setButtons(self):
        self.conn.clicked.connect(self.onConnect)
        self.calibrate.clicked.connect(self.onCalibrate)
        self.start.clicked.connect(self.onStart)
        self.stop.clicked.connect(self.onStop)
        self.reset.clicked.connect(self.onReset)
        self.calibrate.setEnabled(self.has_conn)
        self.start.setEnabled(self.has_calibrated)
        self.stop.setEnabled(self.has_started)
        self.reset.setEnabled(self.has_calibrated)

    def initUI(self):
        self.setButtons()

        layout = QVBoxLayout()
        layout.addWidget(self.conn)
        layout.addWidget(self.calibrate)
        layout.addWidget(self.start)
        layout.addWidget(self.stop)
        layout.addWidget(self.reset)

        self.setGeometry(200, 200, 300, 150)
        self.setLayout(layout)
        self.setWindowTitle('CDN Controller')
        self.show()

    def onCalibrate(self):
        self.has_calibrated = True
        self.start.setEnabled(self.has_calibrated)
        self.reset.setEnabled(self.has_calibrated)
        self.calibrationManager.start_calibration(self.controller, self.detector)
        self.calibrate.setEnabled(not self.has_calibrated)
        self.cv.start()
        

    def onStart(self):
        print("Starting")
        self.has_started = True
        self.detector.is_driving = True
        self.stop.setEnabled(self.has_started)
        self.reset.setEnabled(not self.has_started)
        self.start.setEnabled(not self.has_started)
        

    def onStop(self):
        print("Stopping")
        self.has_started = False
        self.detector.is_driving = False
        self.start.setEnabled(not self.has_started)
        self.reset.setEnabled(self.has_calibrated)
        self.stop.setEnabled(self.has_started)

    def onConnect(self):
        self.has_conn = True
        self.calibrate.setEnabled(self.has_conn)
        self.connectionManager.start_connection()
        self.conn.setEnabled(not self.has_conn)
    
    def onReset(self):
        self.has_calibrated = False
        self.cv.stop()
        self.calibrate.setEnabled(not self.has_calibrated)
        self.start.setEnabled(self.has_calibrated)
        self.stop.setEnabled(self.has_calibrated)
        self.reset.setEnabled(self.has_calibrated)

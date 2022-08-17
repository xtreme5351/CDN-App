from PyQt5.QtWidgets import *
from CDNManagers.calibration import Calibrate
from CDNManagers.connection import Connect


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
        # Bools
        self.has_conn = False
        self.has_calibrated = False
        # Managers
        self.connectionManager = Connect()
        self.calibrationManager = Calibrate()

        self.initUI()

    def setButtons(self):
        self.conn.clicked.connect(self.onConnect)
        self.calibrate.clicked.connect(self.onCalibrate)
        self.start.clicked.connect(self.onStart)
        self.calibrate.setEnabled(self.has_conn)
        self.start.setEnabled(self.has_calibrated)

    def initUI(self):
        self.setButtons()

        layout = QVBoxLayout()
        layout.addWidget(self.conn)
        layout.addWidget(self.calibrate)
        layout.addWidget(self.start)

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

    def onConnect(self):
        self.has_conn = True
        self.calibrate.setEnabled(self.has_conn)
        self.connectionManager.start_connection()

from PyQt5.QtWidgets import *


class CDNApp(QWidget):
    def __init__(self, parent=None):
        if parent is not None:
            super(QWidget, self).__init__(parent)
        else:
            super().__init__()
        self.calibrate = QPushButton("Start calibration")
        self.start = QPushButton("Start driving")
        self.conn = QPushButton("Connect to car")
        self.has_conn = False
        self.has_calibrated = False
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
        print("Calibrating")

    def onStart(self):
        print("Starting")

    def onConnect(self):
        self.has_conn = True
        self.calibrate.setEnabled(self.has_conn)
        print("Connecting")

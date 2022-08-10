from PyQt5.QtWidgets import *


class CDNApp(QWidget):
    def __init__(self, parent=None):
        if parent is not None:
            super(QWidget, self).__init__(parent)
        else:
            super().__init__()
        self.start = QPushButton("Start calibration")
        self.init_ui()

    def init_ui(self):
        self.start.clicked.connect(self.onClicked)

        layout = QVBoxLayout()
        layout.addWidget(self.start)

        self.setGeometry(200, 200, 300, 150)
        self.setLayout(layout)
        self.setWindowTitle('CDN Controller')
        self.show()

    def onClicked(self):
        # self.result.setText("HELLO")
        print("HELLO")

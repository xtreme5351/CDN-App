import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, QUrl, Qt, pyqtSlot

class Helper(QObject):
    @pyqtSlot()
    def OnStart(self):
        print("Start")
    @pyqtSlot()        
    def OnCalibrate(self):
        print("Calibrate")
    @pyqtSlot()
    def OnParameters(self):
        print("Parameters")

app = QGuiApplication(sys.argv)

helper = Helper()

engine = QQmlApplicationEngine()
engine.rootContext().setContextProperty("helper", helper)
engine.load('ball_blender.qml')
engine.quit.connect(app.quit)

sys.exit(app.exec())
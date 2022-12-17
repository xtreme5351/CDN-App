import sys
import os
import threading
import cv2

from PyQt5.QtGui import QGuiApplication, QPixmap, QImage
from PyQt5.QtQml import QQmlApplicationEngine, QQmlProperty
from PyQt5.QtCore import QObject, QUrl, Qt, pyqtSlot, QThread, pyqtSignal

from CDNManagers import CV
from CDNManagers import Detector

def resolve_files(self) -> tuple:
    vid_path = 0
    config_path = os.path.abspath("CDNManagers/data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    model_path = os.path.abspath("CDNManagers/data/frozen_inference_graph.pb")
    classes_path = os.path.abspath("CDNManagers/data/coco.names")
    ui_object = self
    return vid_path, config_path, model_path, classes_path, ui_object

class Helper(QObject):

    def __init__(self, parent=None):
        if parent is not None:
            super(QObject, self).__init__(parent)
        else:
            super().__init__()
        self.detector = Detector(*resolve_files(self))
        self.cv = CV(self.detector, "stop sign")
        self.pix_image = QObject

    def updateImage(self):
        self.pix_image.setProperty("source","file:///" + os.path.abspath("placeholder_image.png"))
        self.pix_image.setProperty("source","file:///" + os.path.abspath("video.png"))

    @pyqtSlot()
    def OnStart(self):
        print("Start")
    @pyqtSlot()
    def OnInitialise(self):
        print("Initialise")
    @pyqtSlot()        
    def OnCalibrate(self):
        print("Calibrate")
        self.cv.start()
    @pyqtSlot()
    def OnParameters(self):
        print("Parameters")

class Blender():
    

    app = QGuiApplication(sys.argv)

    helper = Helper()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("helper", helper)
    engine.load('ball_blender.qml')

    pix_image = None

    if len(engine.rootObjects()) > 0:
        helper.pix_image = engine.rootObjects()[0].findChild(QObject, "pix_image")
        print("obtained")

    engine.quit.connect(app.quit)

    sys.exit(app.exec())
import sys
import os
from threading import Thread
import cv2
from queue import Queue
from time import sleep


from PyQt5.QtGui import QGuiApplication, QPixmap, QImage
from PyQt5.QtQml import QQmlApplicationEngine, QQmlProperty
from PyQt5.QtCore import QObject, QUrl, Qt, pyqtSlot, QThread, pyqtSignal, QTimer

from CDNManagers import CV
from CDNManagers import Detector

def resolve_files(self) -> tuple:
    vid_path = 0
    config_path = os.path.abspath("CDNManagers/data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    model_path = os.path.abspath("CDNManagers/data/frozen_inference_graph.pb")
    classes_path = os.path.abspath("CDNManagers/data/coco.names")
    ui_object = self
    return vid_path, config_path, model_path, classes_path, ui_object

class Worker(QObject):
    rerender = pyqtSignal(int)

    def run(self, cv):
        cv.start()
    
    def RerenderCommand(self, number):
        self.rerender.emit(number)

class Helper(QObject):

    def __init__(self, parent=None):
        if parent is not None:
            super(QObject, self).__init__(parent)
        else:
            super().__init__()
        self.detector = Detector(*resolve_files(self))
        self.cv = CV(self.detector, "stop sign")
        self.pix_image = QObject
        self.rerender = False
        self.render_number = 0

    def updateImage(self):
        self.pix_image.setProperty("source","file:///" + os.path.abspath("video" + str(self.render_number) + ".png"))

    @pyqtSlot()
    def OnStart(self):
        print("Start")
    @pyqtSlot()
    def OnInitialise(self):
        print("Initialise")
        cv_thread = Thread(target = self.cv.start)
        cv_thread.start()
        #self.thread = QThread()
        #self.worker = Worker()
        #self.worker.rerender.connect(self.updateImage)
        #self.worker.moveToThread(self.thread)
        #self.thread.started.connect(self.worker.run(self.cv))
        #self.worker.finished.connect(self.worker.deleteLater)
        #self.thread.finished.connect(self.thread.deleteLater)
        #self.thread.start()
    @pyqtSlot()        
    def OnCalibrate(self):
        print("Calibrate")
        
    @pyqtSlot()
    def OnParameters(self):
        print("Parameters")

    def ExitHandler(self):
        print("Exit")
        self.cv.stop()
        sleep(1)
        if os.path.exists("video0.png"):
            os.remove("video0.png")
        if os.path.exists("video1.png"):
            os.remove("video1.png")

class Blender():
    global helper
    helper = Helper()

    def Update():
        if helper.rerender:
            helper.updateImage()
    app = QGuiApplication(sys.argv)

    
    helper.callback_queue = Queue()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("helper", helper)
    engine.load('ball_blender.qml')

    app.aboutToQuit.connect(helper.ExitHandler)

    pix_image = None
    
    if len(engine.rootObjects()) > 0:
        helper.pix_image = engine.rootObjects()[0].findChild(QObject, "pix_image")
        print("obtained")

    timer = QTimer()
    timer.setInterval(10)
    timer.timeout.connect(Update)
    timer.start()
    
    

    

    engine.quit.connect(app.quit)

    sys.exit(app.exec())
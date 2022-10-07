import os


class CV:
    def __init__(self, _detector):
        self.detector = _detector

    def start(self):
        self.detector.onVideo()

    def stop(self):
        self.detector.offVideo()
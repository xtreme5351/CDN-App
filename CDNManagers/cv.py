import os


class CV:
    def __init__(self, _detector, _tracked_obj):
        self.detector = _detector
        self.tracked_obj = _tracked_obj

    def start(self):
        self.detector.onVideo(self.tracked_obj)

    def stop(self):
        self.detector.offVideo()
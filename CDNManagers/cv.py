from CVDetector import Detector
import os


class CV:
    def __init__(self):
        pass

    @staticmethod
    def get_abs_file_paths(path):
        return os.path.abspath(path)

    def start(self, vid_path=0):
        config_path = self.get_abs_file_paths("CVDetector/data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
        model_path = self.get_abs_file_paths("CVDetector/data/frozen_inference_graph.pb")
        # the above poos when this = os.path.join is used
        #  Hard coded for now, just to make sure it works
        classes_path = self.get_abs_file_paths("CVDetector/data/coco.names")

        detector = Detector(vid_path, config_path, model_path, classes_path)
        detector.onVideo()


def main():
    # vid path 0 represents webcam
    vid_path = 0
    config_path = os.path.join("data", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    model_path = os.path.join("data", "frozen_inference_graph.pb")
    classes_path = os.path.join("data", "coco.names")

    detector = Detector(vid_path, config_path, model_path, classes_path)
    detector.onVideo()


if __name__ == "__main__":
    main()

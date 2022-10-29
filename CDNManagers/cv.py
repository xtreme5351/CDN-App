from CDNManagers import Detector
import os


class CV:
    def __init__(self):
        self.paths = self.resolve_files()
        self.detector = Detector(self.paths[0], self.paths[1], self.paths[2], self.paths[3])

    @staticmethod
    def get_abs_file_paths(path):
        return os.path.abspath(path)

    @staticmethod
    def resolve_files(debug=False):
        vid_path = 0
        if not debug:
            config_path = os.path.abspath("CDNManagers/data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
            model_path = os.path.abspath("CDNManagers/data/frozen_inference_graph.pb")
            # the above absolutely shits itself
            #  Use debug path for now
            classes_path = os.path.abspath("CDNManagers/data/coco.names")
        else:
            print("L tbh, using debug path")
            # config_path = "/Users/pc/PycharmProjects/cdn_app/CDNManagers/data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
            config_path = "/Users/pc/PycharmProjects/cdn_app/CDNManagers/data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
            model_path = "/Users/pc/PycharmProjects/cdn_app/CDNManagers/data/frozen_inference_graph.pb"
            # the above poos when this = os.path.join is used
            #  Hard coded for now, just to make sure it works
            classes_path = "/Users/pc/PycharmProjects/cdn_app/CDNManagers/data/coco.names"
        return vid_path, config_path, model_path, classes_path

    def start(self):
        self.detector.onVideo()

    def stop(self):
        self.detector.offVideo()


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

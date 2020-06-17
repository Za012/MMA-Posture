from PySide2.QtWidgets import QFileDialog
import shutil as sh
import cv2
from openpose import OpenPose
from typing import List
import json
import csv
import os
import calendar
import time


def batch(iterable, n=1):
    length = len(iterable)
    for index in range(0, length, n):
        yield iterable[index: min(index + n, length)]


class KeyPointManager:

    def __init__(self):
        self.files = []
        self.keyPointsLabeled = List[str]
        self.openPoseMap = [
            "Nose",
            "Neck",
            "RShoulder",
            "RElbow",
            "RWrist",
            "LShoulder",
            "LElbow",
            "LWrist",
            "MidHip",
            "RHip",
            "RKnee",
            "RAnkle",
            "LHip",
            "LKnee",
            "LAnkle",
            "REye",
            "LEye",
            "REar",
            "LEar",
            "LBigToe",
            "LSmallToe",
            "LHeel",
            "RBigToe",
            "RSmallToe",
            "RHeel",
            "Background",
        ]
        self.generationDirectory = 'Generated/'
        self.batchName = None
        self.temporaryDirectory = None

    def create_batch_temporary_directory(self):

        if not os.path.exists("temp/"):
            os.mkdir("temp")

        dst = "temp/" + self.batchName + "/"

        if not os.path.exists(dst):
            os.mkdir(dst)

        self.temporaryDirectory = dst

    def copy_files_to_temporary_directory(self):

        for src in self.files:
            print(src)
            split_path = src.split("/")
            sh.copyfile(src, self.temporaryDirectory + split_path[len(split_path) - 1])

    def generate_frames_and_keypoints(self, ui_progress_bar=None):

        if not os.path.exists(self.generationDirectory):
            os.mkdir(self.generationDirectory)

        dst = self.generationDirectory + self.batchName + "/"
        if not os.path.exists(dst):
            os.mkdir(dst)
        
        # Do Openpose on batch on each video and save keypoints
        i = 0
        progress = 5
        for video in os.listdir(self.temporaryDirectory):
            dump_path = dst + "Video" + str(i) + "/"
            while os.path.exists(dump_path):
                i += 1
                dump_path = dst + "Video" + str(i) + "/"
            os.mkdir(dump_path)

            vidcap = cv2.VideoCapture(self.temporaryDirectory + video)
            success, image = vidcap.read()
            count = 0
            progress += len(os.listdir(self.temporaryDirectory))
            while success:
                progress += 10 / progress

                if ui_progress_bar is not None:
                    ui_progress_bar.setValue(progress)

                cv2.imwrite(dump_path + "frame%d.jpg" % count, image)  # save frame as JPEG file
                success, image = vidcap.read()
                count += 1
            i += 1
            vidcap.release()

        if os.path.exists(self.temporaryDirectory):
            sh.rmtree(self.temporaryDirectory)

        op = OpenPose()

        for vidBatch in os.listdir(dst):
            progress += 100 / progress

            if ui_progress_bar is not None:
                ui_progress_bar.setValue(progress)

            keypoint_dst = dst + vidBatch + "/Keypoints"

            if not os.path.exists(keypoint_dst):
                os.mkdir(keypoint_dst)

            print("Processing Batch: " + vidBatch)
            op.pose(dst + vidBatch, keypoint_dst)
            # for each frame Go through openpose and dump output into keypointdst

        if ui_progress_bar is not None:
            ui_progress_bar.setValue(100)

        return dst + "Video" + str(len(os.listdir(dst)) - 1) + "/"

    def read_openpose_json(self, filename: str):

        with open(filename, "rb") as f:
            keypoints_list = []
            keypoints = json.load(f)

            #  assert (
            #           len(keypoints["people"]) > 1  # check this with Zeid
            #   ), "In all pictures, we should have only one person!"

            try:
                keypoints["people"][0]["pose_keypoints_2d"]
            except IndexError:
                print("No people present in given frame")
                return False

            points_2d = keypoints["people"][0]["pose_keypoints_2d"]
            assert (
                    len(points_2d) == 25 * 3
            ), "We have 25 points with (x, y, c); where c is confidence."

            for point_index, (x, y, confidence) in enumerate(batch(points_2d, 3)):
                assert x is not None, "x should be defined"
                assert y is not None, "y should be defined"
                assert confidence is not None, "confidence should be defined"

                keypoints_list.append(
                    {
                        "x": x,
                        "y": y,
                        "c": confidence,
                        "point_label": self.openPoseMap[point_index],
                        "point_index": point_index,
                    }
                )

            return keypoints_list

    def get_keypoint_file(self, file):

        file_path = os.path.basename(file)

        file_directory = os.path.dirname(file)

        filename_noextension = os.path.splitext(file_path)[0]

        keypoints_directory = file_directory + "/Keypoints/"

        file = keypoints_directory + filename_noextension + '_keypoints.json'

        if not os.path.isfile(file):
            print(file + " does not exist")
            return None

        return file

    def write_keypoints_to_csv(self, dataset_file, key_points):
        # process to write to csv file
        with open(dataset_file, 'a', newline='') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=self.openPoseMap)

            # check if file has already been written to
            file_empty = os.stat(dataset_file).st_size == 0

            if file_empty:
                writer.writeheader()  # file doesn't exist yet, write the header

            row_to_write = {}  # variable to store the row we want to write

            # loop through keyPoints and assign the correct body part according to it's index
            for keyPoint in key_points:
                row_to_write.update({self.openPoseMap[keyPoint['point_index']]: "%s,%s,%s" % (
                    keyPoint['x'], keyPoint['y'], keyPoint['c'])
                                     })

            writer.writerow(row_to_write)  # write to row
            print(dataset_file + " was written.")

    def save_files_to_dataset(self, files, labeled=True, directory='Datasets/'):
        print(files)
        # Get current time stamp
        timestamp = calendar.timegm(time.gmtime())

        # Loop through keypoints directory
        for labeled_file in files:

            if labeled is True:
                type = '/' + labeled_file[0]
                file = labeled_file[1]
            else:
                type = ''
                file = labeled_file

            ext = os.path.splitext(file)[-1].lower()

            # check it is a valid file
            if ext != '.jpg' and ext != '.jpeg' and ext != '.png':
                print('Could not convert: ' + file)
                continue

            print('Generating formatted keypoints for... ' + file)

            keypoints_file = self.get_keypoint_file(file)

            # read openpose generated file
            keypoints = self.read_openpose_json(keypoints_file)

            if not keypoints:
                continue

            if not os.path.exists(directory + self.batchName + type + '/'):
                os.makedirs(directory + self.batchName + type + '/')

            # directory of file that will be created
            dataset_file = directory + self.batchName + type + '/dataset_' + str(timestamp) + '.csv'

            # process to write to csv file
            self.write_keypoints_to_csv(dataset_file, keypoints)

        return '/dataset_' + str(timestamp) + '.csv'

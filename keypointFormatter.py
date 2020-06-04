# This Python file uses the following encoding: utf-8
import scipy.io
from tqdm import tqdm
import scipy.io
from tqdm import tqdm
from typing import List, Dict, Any
import json
import glob
import csv
import os
import calendar
import time


def batch(iterable, n=1):
    length = len(iterable)
    for index in range(0, length, n):
        yield iterable[index: min(index + n, length)]


class KeyPointFormatter:

    def __init__(self):
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

    def read_openpose_json(self, filename: str) -> List[Dict[str, Any]]:
        with open(filename, "rb") as f:
            keypoints_list = []
            keypoints = json.load(f)

            #  assert (
            #           len(keypoints["people"]) > 1  # check this with Zeid
            #   ), "In all pictures, we should have only one person!"

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

        return keypoints_directory + filename_noextension + '_keypoints.json'

    def save_to_dataset(self, labeled_files, directory='Datasets/'):

        # Get current time stamp
        timestamp = calendar.timegm(time.gmtime())

        # Loop through keypoints directory
        for labeled_file in labeled_files:

            type = labeled_file[0]
            file = labeled_file[1]

            ext = os.path.splitext(file)[-1].lower()

            # check it is a valid file
            if ext != '.jpg' and ext != '.jpeg' and ext != '.png':
                print('Could not convert: ' + file)
                continue

            print('Generating formatted keypoints for... ' + file)

            keyPointfile = self.get_keypoint_file(file)

            # read openpose generated file
            keyPoints = self.read_openpose_json(keyPointfile)

            if not os.path.exists(directory + type + '/'):
                os.makedirs(directory + type + '/')

            # directory of file that will be created
            dataset_file = directory + type + '/dataset_' + str(timestamp) + '.csv'

            # process to write to csv file
            with open(dataset_file, 'a', newline='') as csvfile:

                writer = csv.DictWriter(csvfile, fieldnames=self.openPoseMap)

                # check if file has already been written to
                file_empty = os.stat(dataset_file).st_size == 0

                if file_empty:
                    writer.writeheader()  # file doesn't exist yet, write the header

                row_to_write = {}  # variable to store the row we want to write

                # loop through keyPoints and assign the correct body part according to it's index
                for keyPoint in keyPoints:
                    row_to_write.update({self.openPoseMap[keyPoint['point_index']]: {
                        "x": keyPoint['x'],
                        "y": keyPoint['y'],
                        "c": keyPoint['c'],
                    }})

                writer.writerow(row_to_write)  # write to row
                print(dataset_file + " was written.")

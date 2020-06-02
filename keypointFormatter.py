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


class KeyPointFormatter:

    OpenPoseMap = [
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

    def batch(iterable, n=1):
        length = len(iterable)
        for index in range(0, length, n):
            yield iterable[index: min(index + n, length)]

    def read_openpose_json(filename: str) -> List[Dict[str, Any]]:
        with open(filename, "rb") as f:
            keypoints_list = []
            keypoints = json.load(f)
            assert (
                    len(keypoints["people"]) > 1  # check this with Zeid
            ), "In all pictures, we should have only one person!"

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
                        "point_label": OpenPoseMap[point_index],
                        "point_index": point_index,
                    }
                )

            return keypoints_list

    def get_all_openpose_json_files() -> List[str]:
        # ... implement your files loader here ...
        return glob.glob("Generated/HenryTest/Video1/Keypoints/*.json")

    def save_to_dataset(directory):

        timestamp = calendar.timegm(time.gmtime())

        for filename in get_all_openpose_json_files():

            keypoints = read_openpose_json(filename)

            datasetFile = directory + 'dataset_' + timestamp + '.csv'

            with open(datasetFile, 'a', newline='') as csvfile:

                fileEmpty = os.stat(datasetFile).st_size == 0

                writer = csv.DictWriter(csvfile, fieldnames=OpenPoseMap)

                if fileEmpty:
                    writer.writeheader()  # file doesn't exist yet, write a header

                rowToWrite = {}

                for keypoint in keypoints:
                    rowToWrite.update({OpenPoseMap[keypoint['point_index']]: {
                        "x": keypoint['x'],
                        "y": keypoint['y'],
                        "c": keypoint['c'],
                    }})

                writer.writerow(rowToWrite)

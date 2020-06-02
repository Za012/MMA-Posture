# From Python
# It requires OpenCV installed for Python
import sys
#import cv2
import os
from sys import platform
import argparse


class OpenPose:
    def __init__(self):
        dir_path = os.getcwd()
        print(os.getcwd())
        try:
            # Windows Import
            if platform == "win32":
                # Change these variables to point to the correct folder (Release/x64 etc.)
                sys.path.append(dir_path + '/openpose/build/python/openpose/Release');
                os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/openpose/build/x64/Release;' + dir_path + '/openpose/build/bin;'
                import pyopenpose as op
                self.op = op
                print("PyOpenPose imported")
                # Win32 is the only supported os for now..
        except ImportError as e:
            print(
                'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e

    def pose(self, image, output):
        try:
            # Custom Params (refer to include/openpose/flags.hpp for more parameters)
            params = dict()
            params["model_folder"] = "openpose/models/"
            params["image_dir"] = image
            params["write_json"] = output

            # Starting OpenPose
            opWrapper = self.op.WrapperPython(3)
            opWrapper.configure(params)
            opWrapper.execute()
        except Exception as e:
            print(e)
            sys.exit(-1)

# This Python file uses the following encoding: utf-8
import string
from random import random

from PySide2.QtWidgets import QFileDialog
import shutil as sh
import os
import cv2
import numpy as np
from openpose import OpenPose
from keypointGen import KeyPointGenerator
from keypointFormatter import KeyPointFormatter
import glob
from PySide2.QtWidgets import QFileDialog, QListWidget, QListWidgetItem, QAbstractItemView
from PySide2 import QtGui
import pandas as pd
from keras.models import load_model
from decimal import Decimal


class FramePredictor:
    PREDICT_DIRECTORY = 'Predict/'

    def __init__(self, ui):
        self.ui = ui
        self.files = []
        self.selectedDirectory = None
        self.keypointFormatter = KeyPointFormatter()
        self.batchName = None
        self.selectedModel = None
        self.filesPredicted = None

        self.ui.predict_filelist.clear()
        self.ui.predict_progressbar.setValue(0)
        print("FramePredictor init")

    def attach(self):
        self.ui.predict_filelist.currentItemChanged.connect(self.itemSelectionChanged)
        self.ui.predict_process_button.clicked.connect(self.process_files)
        self.ui.predict_select_button.clicked.connect(self.select_file)
        self.ui.predict_select_model.clicked.connect(self.select_model)
        self.ui.predict_clear_list.clicked.connect(self.clear)
        self.ui.predict_confidence_label.setText('')
        self.ui.predict_filename_label.setText('')

    def clear(self):
        self.files = []
        self.selectedDirectory = None
        self.batchName = None
        self.selectedModel = None
        self.filesPredicted = None
        self.ui.predict_filelist.clear()

    def check_for_enable_process_button(self):
        self.ui.predict_process_button.setEnabled(self.selectedModel is not None and self.files is not None)

    def select_file(self):
        print("button clicked")

        self.ui.predict_progressbar.setValue(0)
        dialog = QFileDialog.getOpenFileNames()
        self.files += dialog[0]

        if len(self.files) > 0:
            for file in dialog[0]:
                splitfilepath = file.split('/')
                self.ui.filepaths_list.addItem(splitfilepath[len(splitfilepath) - 1])
        self.check_for_enable_process_button()

    def select_model(self):
        print("button clicked")

        self.ui.predict_progressbar.setValue(0)
        dialog = QFileDialog.getOpenFileName()
        self.selectedModel = dialog[0]
        print(self.selectedModel)
        self.check_for_enable_process_button()

    def itemSelectionChanged(self, item):
        if not item:
            return
        for file in self.filesPredicted:
            filename = file[0]
            confidence = file[1]
            splitpath = filename.split('/')
            if splitpath[len(splitpath) - 1] == item.text():
                self.ui.predict_filename_label.setText(str(item.text()))
                self.ui.predict_confidence_label.setText(str(confidence))
                pixmap = QtGui.QPixmap(filename)
                self.ui.predict_image_preview.setPixmap(pixmap)
                self.ui.predict_image_preview.show()

    def display_files_in_ui(self, directory):
        for item in os.listdir(directory):
            extension = item.split('.')
            if extension[len(extension) - 1] == 'jpg' or extension[len(extension) - 1] == 'png' or extension[
                len(extension) - 1] == 'jpeg':
                self.ui.predict_filelist.addItem(ListWidgetItem(item))

        self.ui.predict_filelist.sortItems()
        self.ui.predict_filelist.show()

    def keypointgeneration(self, batchName):

        if not os.path.exists("Generated/"):
            os.mkdir("Generated")
        dst = "Generated/" + batchName + "/"
        if not os.path.exists(dst):
            os.makedirs(dst)
        src = "temp/" + batchName + "/"
        if not os.path.exists(src):
            os.makedirs(src)

        # Do Openpose on batch on each video and save keypoints
        i = 0
        progress = 5
        for video in os.listdir(src):
            dumpPath = dst + "Video" + str(i) + "/"
            while os.path.exists(dumpPath):
                i += 1
                dumpPath = dst + "Video" + str(i) + "/"
            os.mkdir(dumpPath)

            vidcap = cv2.VideoCapture(src + video)
            success, image = vidcap.read()
            count = 0
            progress += len(os.listdir(src))
            while success:
                progress += 10 / progress
                self.ui.predict_progressbar.setValue(progress)
                cv2.imwrite(dumpPath + "frame%d.jpg" % count, image)  # save frame as JPEG file
                success, image = vidcap.read()
                count += 1
            i += 1
            vidcap.release()

        if os.path.exists(src):
            sh.rmtree(src)

        op = OpenPose()

        for vidBatch in os.listdir(dst):
            progress += 100 / progress
            self.ui.predict_progressbar.setValue(progress)
            keypointdst = dst + vidBatch + "/Keypoints"
            if not os.path.exists(keypointdst):
                os.mkdir(keypointdst)

            print("Processing Batch: " + vidBatch)
            op.pose(dst + vidBatch, keypointdst)
            # for each frame Go through openpose and dump output into keypointdst
        self.ui.openpose_progress_p.setValue(100)
        print("DONE, You can now close OpenPose window.")

        return dst

    def format_dataset(self, dataFile):
        dataset = []
        count = 0
        pose = pd.read_csv(dataFile).values


        for row in pose:
            dataset.append([])  # Person (useless dimension, but needed to get 4d)
            personCount = 0
            for person in range(1):
                dataset[count].append([])  # Frame (This is the actual keypoint array (aka 1 row in the excel))
                for cell in row:  # The cell is a string (aka xyc) so we'll split by comma and format each number we get
                    if cell == "0":
                        cell = "0,0,0"
                    if type(cell) != float:
                        buffer = cell.split(',')
                        array = np.empty(shape=len(buffer))  # Was necessary due to it being a float or something
                        i = 0
                        for number in buffer:
                            array[i] = float(number)
                            i += 1
                        # print(array)
                        dataset[count][personCount].append(array)  # Put it in the main dataset
                personCount += 1
            count += 1
        return np.array(dataset)  # Parse it into a numpy array and return!
        # (It was a Python array in the beginning)
        # Reason why it's like this is due to the 'efficency' of numpy arrays makes them not able to
        # have data appended to them, the size of the array has to be known.
        # But Python array is easier to work with in this case

    def predict(self, value_to_predict):
        if not self.selectedModel:
            print('no model selected')
            return None

        loaded_model = load_model(self.selectedModel)
        results = loaded_model.predict(value_to_predict)

        labels = np.argmax(results, axis=1)
        count = 0
        for result in results:
            x = Decimal(result[1] * 100)
            if x < 50:
                return str(labels[count]) + " With " + str(round(x, 2)) + "% Confidence"
            count += 1

    def process_files(self):
        batch_name = self.ui.predict_batch_name.toPlainText()

        if not batch_name:
            print('No batch name received')
            return None

        batch_name = self.PREDICT_DIRECTORY + batch_name

        keypoints_directory = self.keypointgeneration(batch_name)

        if not keypoints_directory:
            print('No keypoints generated')
            return None
        print("directory " + keypoints_directory)

        frame_files = os.listdir(keypoints_directory)

        if not frame_files:
            print('No files in directory')
            return None

        print("frame_files ")
        print(frame_files)

        files_to_predict = []

        # Loop through keypoints directory
        for frameFile in frame_files:
            extension = frameFile.split('.')
            if extension[len(extension) - 1] == 'jpg' or extension[len(extension) - 1] == 'png' or extension[
                len(extension) - 1] == 'jpeg':
                dataset_frame_file = self.keypointFormatter.save_file_to_dataset(keypoints_directory + frameFile, batch_name)
                data_for_prediction = self.format_dataset(dataset_frame_file)
                files_to_predict.append([keypoints_directory + frameFile, data_for_prediction])

        result_files = []

        # Loop through keypoints directory
        for file_to_predict in files_to_predict:
            filename = file_to_predict[0]
            data_for_prediction = file_to_predict[1]

            confidence_string = self.predict(data_for_prediction)
            result_files.append([filename, confidence_string])

        self.filesPredicted = result_files
        self.display_files_in_ui(keypoints_directory)

class ListWidgetItem(QListWidgetItem):
    def __lt__(self, other):
        return float(self.text().split('frame')[1].split('.')[0]) < float(other.text().split('frame')[1].split('.')[0])

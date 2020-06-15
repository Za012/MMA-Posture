# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QFileDialog
import shutil as sh
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelBinarizer as LabelBinarizer
from sklearn.model_selection import train_test_split

import cv2
import re

import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Flatten, Dense, Dropout, Activation
from tensorflow.keras.regularizers import l2


class Teach:

    def __init__(self, ui):
        self.ui = ui
        self.files = []
        self.ui.filepaths_list.clear()
        self.ui.openpose_progress.setValue(0)
        self.ui.status_label.setText("Import Files please")
        self.ui.process_button.setEnabled(False)
        self.data_folder_path = 'datasets/'
        print("Keypointgen init")

    def attach(self):
        self.ui.datasetSelectBtn.clicked.connect(self.selectDatasetDirectory)
        self.ui.teachBtn.clicked.connect(self.teach)
        # add list clear btn / also clears self.files

    def selectDatasetDirectory(self):
        dirs = QFileDialog.getExistingDirectory()
        print(dirs)
        pathArray = dirs.split('/')
        self.batchName = pathArray[len(pathArray) - 1]
        print("Selected Batch: " + self.batchName)

        self.postures = os.listdir(dirs)
        self.data = []
        count = 0
        self.labels = []
        for pose in self.postures:
            print(pose)
            fileNames = os.listdir(self.data_folder_path+self.batchName+'/'+pose)
            print(pose + "/" + str(fileNames))
            for file in fileNames:
                print("Processing: " + file)
                self.data.append(pd.read_csv(self.data_folder_path + self.batchName +'/'+ pose + "/" + file).values)
                for i in range(len(self.data[count])):
                    self.labels.append(pose)
                print(i)
                print(len(self.data[count]))
                count += 1

        self.ui.batchNameLabel.setText(self.batchName)

    def teach(self):
        ds = self.formatDataset(self.data)
        lb = LabelBinarizer()
        labels = lb.fit_transform(self.labels)

        # split data into train and test
        print(len(labels))
        print(len(ds))

        (trainX, testX, trainY, testY) = train_test_split(ds, labels, test_size=0.25, stratify=labels, random_state=42)

        print("SHAPES")
        print("ORIGINAL SHAPE: " + str(ds.shape))
        print("TRAIN SINGLE SHAPE: " + str(trainX[0].shape))
        print("TRAIN ARRAY SHAPE: " + str(trainX.shape))
        print("TEST SINGLE SHAPE: " + str(testX[0].shape))
        print("TEST ARRAY SHAPE: " + str(testX.shape))
        modelName = self.ui.modelName.toPlainText()
        if not modelName:
            self.ui.outputLabel.setText("Enter a model name")
            return

        model = self.modelInit()
        self.ui.outputLabel.setText("PROCESSING")
        history = model.fit(trainX, trainY, batch_size=32,
                            validation_data=(testX, testY), epochs=20)  # Change to 20 epochs when testing
        print("TRAINING COMPLETE")
        self.ui.outputLabel.setText("COMPLETE")

        if not os.path.exists("Models/"+self.batchName):
            os.makedirs("Models/"+self.batchName)

        model.save('Models/' + self.batchName + '/'+modelName+".h5")


    def formatDataset(self,data):
        dataset = []
        count = 0
        for pose in data:
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


    def modelInit(self):
        # CONFIGS
        init = "he_normal"
        reg = l2(0.0005)
        inputShape = (1, 25, 3)
        chanDim = -1
        classes = len(self.postures)  # len of labels (2 for now)
        ####

        model = Sequential()

        # This is mostly copied for Kim's link, I only changed the Conv2D things the example: (1,4)
        # 16 FILTERS
        # 7x7 filters -- 2x2 strides
        # the spatial dimensions of the volume
        model.add(Conv2D(16, (1, 4), strides=(2, 2), padding="valid",
                         kernel_initializer=init, kernel_regularizer=reg,
                         input_shape=inputShape))
        # here we stack two CONV layers on top of each other where
        # each layerswill learn a total of 32 (3x3) filters
        model.add(Conv2D(32, (3, 3), padding="same",
                         kernel_initializer=init, kernel_regularizer=reg))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(32, (3, 3), strides=(2, 2), padding="same",
                         kernel_initializer=init, kernel_regularizer=reg))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Dropout(0.25))

        # stack two more CONV layers, keeping the size of each filter

        # as 3x3 but increasing to 64 total learned filters
        model.add(Conv2D(64, (2, 2), padding="same",
                         kernel_initializer=init, kernel_regularizer=reg))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(64, (2, 6), strides=(2, 2), padding="same",
                         kernel_initializer=init, kernel_regularizer=reg))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Dropout(0.25))

        # increase the number of filters again, this time to 128
        model.add(Conv2D(128, (6, 4), padding="same",
                         kernel_initializer=init, kernel_regularizer=reg))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))

        model.add(Conv2D(128, (3, 3), strides=(2, 2), padding="same",
                         kernel_initializer=init, kernel_regularizer=reg))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Dropout(0.25))

        # fully-connected layer
        model.add(Flatten())
        model.add(Dense(512, kernel_initializer=init))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))
        # softmax classifier
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        print("MODEL PREPARED")
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        print("MODEL COMPILED")
        return model

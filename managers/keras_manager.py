# This Python file uses the following encoding: utf-8
import numpy as np
from keras.models import load_model
from sklearn.preprocessing import LabelBinarizer as LabelBinarizer
from sklearn.model_selection import train_test_split

import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Flatten, Dense, Dropout, Activation
from tensorflow.keras.regularizers import l2
from decimal import Decimal

import os
import pandas as pd


class KerasManager:

    def __init__(self):
        self.model = None
        self.model_name = None
        self.labels = ['guard', 'jab', 'upper']
        self.postures = []

    def load_model(self, model_name):
        if self.model_name == model_name:
            return
        self.model_name = model_name
        self.model = load_model(self.model_name)

    def predict(self, value_to_predict, frame_files):
        results = self.model.predict(value_to_predict)

        indexed_results = []

        labels = np.argmax(results, axis=1)
        count = 0
        for result in results:
            indexed_results.append(
                [frame_files[count], # index of frame
                 "Likely a " + self.labels[labels[count]] + " with a confidence of " \
                 + str(round(Decimal(result[labels[count]] * 100), 2)) # condifence level
                 ]
            )
            count += 1
        print(indexed_results)
        return indexed_results

    def model_init(self):
        # CONFIGS
        init = "he_normal"
        reg = l2(0.001)
        input_shape = (1, 25, 3)
        classes = len(self.postures)  # len of labels (3 for now)

        model = Sequential()

        # 16 FILTERS
        # 7x7 filters -- 2x2 strides
        # the spatial dimensions of the volume
        model.add(Conv2D(16, (1, 4), strides=(2, 2), padding="valid",
                         kernel_initializer=init, kernel_regularizer=reg,
                         input_shape=input_shape))
        # here we stack two CONV layers on top of each other where
        # each layerswill learn a total of 32 (3x3) filters
        model.add(Conv2D(32, (3, 3), padding="same",
                         kernel_initializer=init, kernel_regularizer=reg))
        model.add(Activation("relu"))

        model.add(Conv2D(32, (3, 3), strides=(2, 2), padding="same",
                         kernel_initializer=init, kernel_regularizer=reg))
        model.add(Activation("relu"))

        model.add(Dropout(0.25))

        # stack two more CONV layers, keeping the size of each filter

        # as 3x3 but increasing to 64 total learned filters
        model.add(Conv2D(64, (2, 2), padding="same",
                         kernel_initializer=init, kernel_regularizer=reg))
        model.add(Activation("relu"))
        model.add(Conv2D(64, (2, 6), strides=(2, 2), padding="same",
                         kernel_initializer=init, kernel_regularizer=reg))
        model.add(Activation("relu"))
        model.add(Dropout(0.25))

        # increase the number of filters again, this time to 128
        model.add(Conv2D(128, (6, 4), padding="same",
                         kernel_initializer=init, kernel_regularizer=reg))
        model.add(Activation("relu"))

        model.add(Conv2D(128, (3, 3), strides=(2, 2), padding="same",
                         kernel_initializer=init, kernel_regularizer=reg))
        model.add(Activation("relu"))
        model.add(Dropout(0.25))

        # fully-connected layer
        model.add(Flatten())
        model.add(Dense(512, kernel_initializer=init))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))
        # softmax classifier
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        print("MODEL PREPARED")

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        print("MODEL COMPILED")

        self.model = model

        return model

    def teach(self, model_name, dataset, batchname, output_label=None):
        lb = LabelBinarizer()
        labels = lb.fit_transform(self.labels)

        # split data into train and test
        print(len(labels))
        print(len(dataset))

        (trainX, testX, trainY, testY) = train_test_split(dataset, labels, test_size=0.25, stratify=self.labels,
                                                          random_state=42)

        print("SHAPES")
        print("ORIGINAL SHAPE: " + str(dataset.shape))
        print("TRAIN SINGLE SHAPE: " + str(trainX[0].shape))
        print("TRAIN ARRAY SHAPE: " + str(trainX.shape))
        print("TEST SINGLE SHAPE: " + str(testX[0].shape))
        print("TEST ARRAY SHAPE: " + str(testX.shape))

        model = self.model_init()

        if output_label is not None:
            output_label.setText("PROCESSING")

        model.fit(trainX, trainY, batch_size=32,
                  validation_data=(testX, testY), epochs=20)  # Change to 20 epochs when testing

        print("TRAINING COMPLETE")
        if output_label is not None:
            output_label.setText("COMPLETE")

        if not os.path.exists("Models/" + batchname):
            os.makedirs("Models/" + batchname)

        model.save('Models/' + batchname + '/' + model_name + ".h5")

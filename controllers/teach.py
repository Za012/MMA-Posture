# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QFileDialog

import os
import pandas as pd

from managers.format_manager import FormatManager
from managers.keras_manager import KerasManager


class Teach:

    def __init__(self, ui):
        self.ui = ui
        self.postures = None
        self.batchName = None
        self.data = None
        self.labels = None

        self.kerasManager = KerasManager()

        self.ui.filepaths_list.clear()
        self.ui.openpose_progress.setValue(0)
        self.ui.status_label.setText("Import Files please")
        self.ui.process_button.setEnabled(False)
        self.data_folder_path = 'datasets/'
        print("Teach init")

    def attach(self):
        self.ui.datasetSelectBtn.clicked.connect(self.select_dataset_directory)
        self.ui.teachBtn.clicked.connect(self.teach)

    def select_dataset_directory(self):
        dirs = QFileDialog.getExistingDirectory(None, 'Select a batch', 'Datasets/')
        if not dirs:
            return

        print(dirs)

        path_array = dirs.split('/')
        self.batchName = path_array[len(path_array) - 1]
        print("Selected Batch: " + self.batchName)

        self.postures = os.listdir(dirs)
        self.data = []
        count = 0
        self.labels = []
        for pose in self.postures:
            print(pose)
            file_names = os.listdir(self.data_folder_path + self.batchName + '/' + pose)
            print(pose + "/" + str(file_names))
            for file in file_names:
                print("Processing: " + file)
                self.data.append(pd.read_csv(self.data_folder_path + self.batchName + '/' + pose + "/" + file).values)
                for i in range(len(self.data[count])):
                    self.labels.append(pose)
                    print(i)
                    print(len(self.data[count]))
                count += 1

        self.ui.batchNameLabel.setText(self.batchName)

    def teach(self):

        model_name = self.ui.modelName.toPlainText()
        if not model_name:
            self.ui.outputLabel.setText("Enter a model name")
            return

        print(self.data)
        ds = FormatManager.format_dataset(self.data, False)
        self.kerasManager.labels = self.labels
        self.kerasManager.postures = self.postures
        self.kerasManager.teach(model_name, ds, self.batchName, self.ui.outputLabel)

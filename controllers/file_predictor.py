# This Python file uses the following encoding: utf-8
import os
from PySide2.QtWidgets import QFileDialog, QListWidgetItem
from PySide2 import QtGui


from managers.keypoint_manager import KeyPointManager
from managers.format_manager import FormatManager
from managers.keras_manager import KerasManager


class FramePredictor:
    PREDICT_DIRECTORY = 'Predict/'
    DATASET_RESULTS_DIRECTORY = 'Results/'

    def __init__(self, ui):
        self.ui = ui
        self.files = []
        self.selectedDirectory = None
        self.keypointManager = KeyPointManager()
        self.kerasManager = KerasManager()
        self.selectedModel = None
        self.filesPredicted = None

        self.ui.predict_filelist.clear()
        self.ui.predict_progressbar.setValue(0)
        print("FilePredictor init")

    def attach(self):
        self.ui.predict_filelist.currentItemChanged.connect(self.item_selection_changed)
        self.ui.predict_process_button.clicked.connect(self.process_files)
        self.ui.predict_select_button.clicked.connect(self.select_file)
        self.ui.predict_select_model.clicked.connect(self.select_model)
        self.ui.predict_clear_list.clicked.connect(self.clear)
        self.ui.tabWidget.currentChanged.connect(self.check_tab_open)
        self.ui.predict_confidence_label.setText('')

    def check_tab_open(self):
        if self.ui.modelName.toPlainText() is not None and self.ui.modelName.toPlainText() is not '':
            self.ui.predict_batch_name.setText(self.ui.modelName.toPlainText())
            self.ui.predict_batch_name.setEnabled(False)
        else:
            self.ui.predict_batch_name.setEnabled(True)
            self.ui.predict_batch_name.setText('')

    def clear(self):
        self.files = []
        self.selectedDirectory = None
        self.selectedModel = None
        self.filesPredicted = None
        self.ui.predict_filelist.clear()

    def check_for_enable_process_button(self):
        self.ui.predict_process_button.setEnabled(self.selectedModel is not None and self.files is not None)

    def select_file(self):
        self.ui.predict_progressbar.setValue(0)
        dialog = QFileDialog.getOpenFileNames()
        self.files += dialog[0]

        if len(self.files) > 0:
            for file in dialog[0]:
                splitfilepath = file.split('/')
                self.ui.filepaths_list.addItem(splitfilepath[len(splitfilepath) - 1])
        self.check_for_enable_process_button()

    def select_model(self):
        self.ui.predict_progressbar.setValue(0)
        dialog = QFileDialog.getOpenFileName()
        self.selectedModel = dialog[0]
        self.check_for_enable_process_button()

    def item_selection_changed(self, item):
        if not item:
            return
        for file in self.filesPredicted:
            filename = file[0]
            confidence = file[1]
            if os.path.basename(filename) == item.text():
                print(file)
                self.ui.predict_filename_label.setText(str(os.path.basename(item.text())))
                self.ui.predict_confidence_label.setText(str(confidence))
                pixmap = QtGui.QPixmap(filename)
                self.ui.predict_image_preview.setPixmap(pixmap)
                self.ui.predict_image_preview.show()

    def display_files_in_list(self, files):
        for item in files:
            self.ui.predict_filelist.addItem(ListWidgetItem(os.path.basename(item)))
        self.ui.predict_filelist.sortItems()
        self.ui.predict_filelist.show()

    def process_files(self):
        batch_name = self.ui.predict_batch_name.toPlainText()

        if not batch_name:
            print('No batch name received')
            return None

        if not self.selectedModel:
            print('No model received')
            return None

        self.keypointManager.batchName = self.PREDICT_DIRECTORY + batch_name
        self.keypointManager.files = self.files
        self.keypointManager.create_batch_temporary_directory()
        self.keypointManager.create_batch_temporary_directory()
        keypoints_directory = self.keypointManager.generate_frames_and_keypoints(self.ui.predict_progressbar)

        if not keypoints_directory:
            print('No keypoints generated')
            return None

        frame_files = [os.path.abspath(os.path.join(keypoints_directory, p)) for p in os.listdir(keypoints_directory) if
                       p.endswith('jpg') or p.endswith('png')]

        if not frame_files:
            print('No files in directory')
            return None

        dataset_file = self.keypointManager.save_files_to_dataset(frame_files, False, self.DATASET_RESULTS_DIRECTORY)

        data_for_prediction = FormatManager.format_dataset(self.DATASET_RESULTS_DIRECTORY + self.PREDICT_DIRECTORY + batch_name + dataset_file)

        self.kerasManager.load_model(self.selectedModel)
        result_files = self.kerasManager.predict(data_for_prediction, frame_files)

        self.filesPredicted = result_files
        self.display_files_in_list(frame_files)


class ListWidgetItem(QListWidgetItem):
    def __lt__(self, other):
        return float(self.text().split('frame')[1].split('.')[0]) < float(other.text().split('frame')[1].split('.')[0])

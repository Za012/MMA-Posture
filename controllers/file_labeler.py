# This Python file uses the following encoding: utf-8
from PySide2 import QtGui
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QFileDialog, QListWidgetItem
import os
from managers.keypoint_manager import KeyPointManager


class FileLabeler:
    def __init__(self, ui):
        self.ui = ui
        self.selectedDirectory = None
        self.filelistpaths = []
        self.selectedPaths = []
        self.labeledFrames = []
        self.keyPointManager = KeyPointManager()
        print("FileLabeler init")

    def attach(self):
        self.ui.fileList.currentItemChanged.connect(self.item_selection_changed)
        self.ui.btnSelectDirectory.clicked.connect(self.directory_button_clicked)
        self.ui.btnUppercut.clicked.connect(self.uppercut_button_clicked)
        self.ui.btnGuard.clicked.connect(self.guard_button_clicked)
        self.ui.btnJab.clicked.connect(self.jab_button_clicked)
        self.ui.generateDatasetButton.clicked.connect(self.generate_button_clicked)
        self.ui.generateDatasetButton.setEnabled(False)
        self.ui.btnDeselect.clicked.connect(self.deselect_button_clicked)

    def uppercut_button_clicked(self):
        self.add_labeled_frames_to_array("uppercut", QColor(255, 150, 0, 160))

    def guard_button_clicked(self):
        self.add_labeled_frames_to_array("guard", QColor(105, 155, 103, 127))

    def jab_button_clicked(self):
        self.add_labeled_frames_to_array("jab", QColor(255, 0, 0, 127))

    def generate_button_clicked(self):
        self.keyPointManager.save_files_to_dataset(self.labeledFrames)
        self.clear()

    def deselect_button_clicked(self):
        for item in self.ui.fileList.selectedItems():
            for labeled in self.labeledFrames:
                split = labeled[1].split('/')
                if item.text() == split[len(split)-1]:
                    self.labeledFrames.remove(labeled)

            item.setBackground(QColor(0,0,0,0))
            item.setSelected(False)

    def item_selection_changed(self, item):
        if not item:
            return
        for path in self.filelistpaths:
            splitpath = path.split('/')
            if splitpath[len(splitpath) - 1] == item.text():
                self.ui.lblSelectedFile.setText(str(item.text()))
                pixmap = QtGui.QPixmap(path)
                self.ui.imagePreview.setPixmap(pixmap)
                self.ui.imagePreview.show()

    def directory_button_clicked(self):
        self.clear()
        dialog = QFileDialog.getExistingDirectory()
        self.selectedDirectory = dialog

        for item in os.listdir(dialog):
            extension = item.split('.')
            if extension[len(extension) - 1] == 'jpg' or extension[len(extension) - 1] == 'png' or extension[
                len(extension) - 1] == 'jpeg':
                self.ui.fileList.addItem(ListWidgetItem(item))

        for file in os.listdir(dialog):
            self.filelistpaths.append(dialog + "/" + file)

        splitdirpath = dialog.split("/")
        self.ui.lblSelectedDirectory.setText(splitdirpath[len(splitdirpath) - 1])

        self.keyPointManager.batchName = splitdirpath[len(splitdirpath) - 2]
        # enable/disable generated button
        self.ui.generateDatasetButton.setEnabled(self.selectedDirectory is not None)
        self.ui.fileList.sortItems()
        self.ui.fileList.show()

    def clear(self):
        self.labeledFrames.clear()
        self.ui.fileList.clear()
        self.selectedDirectory = None
        self.filelistpaths.clear()

    def add_labeled_frames_to_array(self, pose, color):
        for item in self.ui.fileList.selectedItems():
            for path in self.filelistpaths:
                splitpath = path.split('/')
                if splitpath[len(splitpath) - 1] == item.text():
                    self.check_labeled_array_for_duplicated(path)
                    self.labeledFrames.append([pose, path])
            item.setBackground(color)
            item.setSelected(False)

    def check_labeled_array_for_duplicated(self, path):
        for labeled in self.labeledFrames:
            if path in labeled[1]:
                self.labeledFrames.remove(labeled)

class ListWidgetItem(QListWidgetItem):
    def __lt__(self, other):
        return float(self.text().split('frame')[1].split('.')[0]) < float(other.text().split('frame')[1].split('.')[0])
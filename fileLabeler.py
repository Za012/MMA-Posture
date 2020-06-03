# This Python file uses the following encoding: utf-8
from PySide2 import QtGui
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QFileDialog
import os

from keypointFormatter import KeyPointFormatter


class FileLabeler:
    def __init__(self, ui):
        self.ui = ui
        self.selectedDirectory = None
        self.filelistpaths = []
        self.selectedPaths = []
        self.labeledFrames = []
        self.keyPointFormatter = KeyPointFormatter()

    def attach(self):
        self.ui.fileList.currentItemChanged.connect(self.itemSelectionChanged)
        self.ui.btnSelectDirectory.clicked.connect(self.directoryButtonClicked)
        self.ui.btnGuard.clicked.connect(self.guardButtonClicked)
        self.ui.btnJab.clicked.connect(self.jabButtonClicked)
        self.ui.generateDatasetButton.clicked.connect(self.generateButtonClicked)
        self.ui.generateDatasetButton.setEnabled(False)

    def guardButtonClicked(self):
        self.addLabeledFramesToArray("guard", QColor(105, 155, 103, 127))

    def jabButtonClicked(self):
        self.addLabeledFramesToArray("jab", QColor(255, 0, 0, 127))

    def addLabeledFramesToArray(self, pose, color):
        for item in self.ui.fileList.selectedItems():
            for path in self.filelistpaths:
                splitpath = path.split('/')
                if splitpath[len(splitpath) - 1] == item.text():
                    self.checkLabeledArrayForDuplicated(path)
                    self.labeledFrames.append([pose, path])
            item.setBackground(color)
            item.setSelected(False)

    def checkLabeledArrayForDuplicated(self, path):
        if ["guard", path] in self.labeledFrames:
            self.labeledFrames.remove(["guard", path])
        if ["jab", path] in self.labeledFrames:
            self.labeledFrames.remove(["jab", path])

    def itemSelectionChanged(self, item):
        for path in self.filelistpaths:
            splitpath = path.split('/')
            if splitpath[len(splitpath) - 1] == item.text():
                self.ui.lblSelectedFile.setText(str(item.text()))
                pixmap = QtGui.QPixmap(path)
                self.ui.imagePreview.setPixmap(pixmap)
                self.ui.imagePreview.show()

    def directoryButtonClicked(self):
        dialog = QFileDialog.getExistingDirectory()
        self.selectedDirectory = dialog
        self.ui.fileList.addItems(os.listdir(dialog))
        for file in os.listdir(dialog):
            self.filelistpaths.append(dialog + "/" + file)
        splitdirpath = dialog.split("/")
        self.ui.lblSelectedDirectory.setText(splitdirpath[len(splitdirpath) - 1])
        # enable/disable generated button
        self.ui.generateDatasetButton.setEnabled(self.selectedDirectory is not None)

    def generateButtonClicked(self):
        self.keyPointFormatter.save_to_dataset(self.labeledFrames)

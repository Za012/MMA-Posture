# This Python file uses the following encoding: utf-8
from PySide2 import QtGui
from PySide2.QtCore import QRect
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QFileDialog, QListWidget, QListWidgetItem, QAbstractItemView
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
        self.ui.btnUppercut.clicked.connect(self.uppercutButtonClicked)
        self.ui.btnGuard.clicked.connect(self.guardButtonClicked)
        self.ui.btnJab.clicked.connect(self.jabButtonClicked)
        self.ui.generateDatasetButton.clicked.connect(self.generateButtonClicked)
        self.ui.generateDatasetButton.setEnabled(False)
        self.ui.btnDeselect.clicked.connect(self.deselectButtonClicked)

    def uppercutButtonClicked(self):
        self.addLabeledFramesToArray("uppercut", QColor(255, 150, 0, 160))

    def guardButtonClicked(self):
        self.addLabeledFramesToArray("guard", QColor(105, 155, 103, 127))

    def jabButtonClicked(self):
        self.addLabeledFramesToArray("jab", QColor(255, 0, 0, 127))

    def generateButtonClicked(self):
        self.keyPointFormatter.save_files_to_dataset(self.labeledFrames,self.batchName)
        self.clear()

    def deselectButtonClicked(self):
        for item in self.ui.fileList.selectedItems():
            for labeled in self.labeledFrames:
                split = labeled[1].split('/')
                if item.text() == split[len(split)-1]:
                    self.labeledFrames.remove(labeled)

            item.setBackground(QColor(0,0,0,0))
            item.setSelected(False)

    def clear(self):
        self.labeledFrames.clear()
        self.ui.fileList.clear()
        self.selectedDirectory = None
        self.filelistpaths.clear()



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
        for labeled in self.labeledFrames:
            if path in labeled[1]:
                self.labeledFrames.remove(labeled)

    def itemSelectionChanged(self, item):
        if not item:
            return
        for path in self.filelistpaths:
            splitpath = path.split('/')
            if splitpath[len(splitpath) - 1] == item.text():
                self.ui.lblSelectedFile.setText(str(item.text()))
                pixmap = QtGui.QPixmap(path)
                self.ui.imagePreview.setPixmap(pixmap)
                self.ui.imagePreview.show()

    def directoryButtonClicked(self):
        self.clear()
        dialog = QFileDialog.getExistingDirectory()
        self.selectedDirectory = dialog

        for item in os.listdir(dialog):
            extension = item.split('.')
            if extension[len(extension)-1] == 'jpg' or extension[len(extension)-1] == 'png' or extension[len(extension)-1] == 'jpeg':
                self.ui.fileList.addItem(ListWidgetItem(item))

        for file in os.listdir(dialog):
            self.filelistpaths.append(dialog + "/" + file)

        splitdirpath = dialog.split("/")
        self.ui.lblSelectedDirectory.setText(splitdirpath[len(splitdirpath) - 1])
        self.batchName = splitdirpath[len(splitdirpath)-2]
        # enable/disable generated button
        self.ui.generateDatasetButton.setEnabled(self.selectedDirectory is not None)
        self.ui.fileList.sortItems()
        self.ui.fileList.show()


class ListWidgetItem(QListWidgetItem):
    def __lt__(self, other):
        return float(self.text().split('frame')[1].split('.')[0]) < float(other.text().split('frame')[1].split('.')[0])
# This Python file uses the following encoding: utf-8
from PySide2 import QtGui
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QFileDialog
import os

class FileLabeler:
    def __init__(self, ui):
        self.ui = ui
        self.filelistpaths = []
        self.selectedPaths = []
        self.labeledFrames = []

    def attach(self):
        self.ui.fileList.currentItemChanged.connect(self.itemSelectionChanged)
        self.ui.btnSelectDirectory.clicked.connect(self.directoryButtonClicked)
        self.ui.btnGuard.clicked.connect(self.guardButtonClicked)
        self.ui.btnJab.clicked.connect(self.jabButtonClicked)

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
        for labeled in self.labeledFrames:
            if path in labeled[1]:
                self.labeledFrames.remove(labeled)

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
        self.ui.fileList.addItems(os.listdir(dialog))
        for file in os.listdir(dialog):
            self.filelistpaths.append(dialog+"/"+file)
        splitdirpath = dialog.split("/")
        self.ui.lblSelectedDirectory.setText(splitdirpath[len(splitdirpath)-1])

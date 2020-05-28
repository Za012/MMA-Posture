# This Python file uses the following encoding: utf-8
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QFileDialog
import os

class FileLabeler:
    def __init__(self, ui):
        self.ui = ui
        self.filelistpaths = []

    def attach(self):
        self.ui.fileList.itemClicked.connect(self.item_click)
        self.ui.btnSelectDirectory.clicked.connect(self.directoryButtonClicked)

    def item_click(self, item):
        for path in self.filelistpaths:
            splitpath = path.split('/')
            if(splitpath[len(splitpath)-1] == item.text()):
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

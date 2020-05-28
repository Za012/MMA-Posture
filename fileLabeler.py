# This Python file uses the following encoding: utf-8
from PySide2 import QtCore, QtGui, QtWidgets

class FileLabeler:
    def __init__(self, ui):
        self.ui = ui
        print("file labeler init")

        frames = ["Frame1", "Frame2", "Frame3", "Frame4"]
        self.ui.fileList.addItems(frames)

    def attach(self):
        self.ui.fileList.itemClicked.connect(self.item_click)

    def item_click(self, item):
        self.ui.lblSelectedFile.setText(str(item.text()))
        pixmap = QtGui.QPixmap(str(item.text())+'.png')
        self.ui.imagePreview.setPixmap(pixmap)
        self.ui.imagePreview.show()

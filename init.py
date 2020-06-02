# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from ui_mainwindow import Ui_MainWindow
from keypointGen import KeyPointGenerator


class init(QMainWindow):
    def __init__(self):
        app = QApplication([])
        print("init")
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        QMainWindow.show(self)

        #   INSTANTIATE GUI BACKEND
        # KeyPoint Generator
        keyGen = KeyPointGenerator(self.ui)
        keyGen.attach()

        sys.exit(app.exec_())

if __name__ == "__main__":
    init()



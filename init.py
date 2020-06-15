# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from ui_mainwindow import Ui_MainWindow
from keypointGen import KeyPointGenerator
from fileLabeler import FileLabeler
from teach import Teach


class init(QMainWindow):
    def __init__(self):
        app = QApplication([])
        print("init")
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)



        #   INSTANTIATE GUI BACKEND
        # KeyPoint Generator
        keyGen = KeyPointGenerator(self.ui)
        keyGen.attach()

        # File labeler
        labeler = FileLabeler(self.ui)
        labeler.attach()

        # Teacher
        teach = Teach(self.ui)
        teach.attach()

        QMainWindow.show(self)
        sys.exit(app.exec_())



if __name__ == "__main__":
    init()



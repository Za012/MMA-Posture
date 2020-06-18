# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from ui_mainwindow import Ui_MainWindow
from controllers.keypoint_generator import KeyPointGenerator
from controllers.file_labeler import FileLabeler
from controllers.file_predictor import FramePredictor
from controllers.teach import Teach


class init(QMainWindow):
    def __init__(self):
        app = QApplication([])
        print("init")
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #   INSTANTIATE GUI BACKEND
        # KeyPoint Generator
        key_gen = KeyPointGenerator(self.ui)
        key_gen.attach()

        # File labeler
        labeler = FileLabeler(self.ui)
        labeler.attach()

        # Teacher
        teach = Teach(self.ui)
        teach.attach()

        # Teacher
        frame_predictor = FramePredictor(self.ui)
        frame_predictor.attach()

        QMainWindow.show(self)
        sys.exit(app.exec_())


if __name__ == "__main__":
    init()

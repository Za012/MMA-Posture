# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from ui_mainwindow import Ui_MainWindow


class init(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QApplication([])
    window = init()
    window.show()
    sys.exit(app.exec_())

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(922, 581)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.openpose = QWidget()
        self.openpose.setObjectName(u"openpose")
        self.import_button = QPushButton(self.openpose)
        self.import_button.setObjectName(u"import_button")
        self.import_button.setGeometry(QRect(381, 110, 120, 41))
        font = QFont()
        font.setPointSize(10)
        self.import_button.setFont(font)
        self.process_button = QPushButton(self.openpose)
        self.process_button.setObjectName(u"process_button")
        self.process_button.setGeometry(QRect(390, 260, 101, 40))
        self.process_button.setFont(font)
        self.openpose_progress = QProgressBar(self.openpose)
        self.openpose_progress.setObjectName(u"openpose_progress")
        self.openpose_progress.setGeometry(QRect(280, 310, 331, 23))
        self.openpose_progress.setValue(24)
        self.status_label = QLabel(self.openpose)
        self.status_label.setObjectName(u"status_label")
        self.status_label.setGeometry(QRect(206, 390, 471, 51))
        font1 = QFont()
        font1.setPointSize(13)
        self.status_label.setFont(font1)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.filepaths_list = QListWidget(self.openpose)
        QListWidgetItem(self.filepaths_list)
        self.filepaths_list.setObjectName(u"filepaths_list")
        self.filepaths_list.setGeometry(QRect(60, 190, 151, 192))
        self.clear_button = QPushButton(self.openpose)
        self.clear_button.setObjectName(u"clear_button")
        self.clear_button.setGeometry(QRect(60, 150, 151, 31))
        self.clear_button.setFont(font)
        self.batch_name = QTextEdit(self.openpose)
        self.batch_name.setObjectName(u"batch_name")
        self.batch_name.setGeometry(QRect(370, 190, 141, 31))
        self.batch_name.setFont(font)
        self.batch_name_label = QLabel(self.openpose)
        self.batch_name_label.setObjectName(u"batch_name_label")
        self.batch_name_label.setGeometry(QRect(380, 168, 121, 20))
        self.batch_name_label.setFont(font)
        self.batch_name_label.setAlignment(Qt.AlignCenter)
        self.tabWidget.addTab(self.openpose, "")
        self.labeler = QWidget()
        self.labeler.setObjectName(u"labeler")
        self.fileList = QListWidget(self.labeler)
        self.fileList.setObjectName(u"fileList")
        self.fileList.setGeometry(QRect(20, 120, 241, 351))
        self.fileList.setAlternatingRowColors(True)
        self.fileList.setSelectionMode(QAbstractItemView.MultiSelection)
        self.btnGuard = QPushButton(self.labeler)
        self.btnGuard.setObjectName(u"btnGuard")
        self.btnGuard.setGeometry(QRect(690, 70, 81, 31))
        self.btnGuard.setStyleSheet(u"background-color: rgba(105, 155, 103, 160); border: none;")
        self.btnSelectDirectory = QPushButton(self.labeler)
        self.btnSelectDirectory.setObjectName(u"btnSelectDirectory")
        self.btnSelectDirectory.setGeometry(QRect(20, 80, 91, 23))
        self.imagePreview = QLabel(self.labeler)
        self.imagePreview.setObjectName(u"imagePreview")
        self.imagePreview.setGeometry(QRect(380, 120, 501, 351))
        self.imagePreview.setScaledContents(True)
        self.label = QLabel(self.labeler)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 20, 281, 31))
        font2 = QFont()
        font2.setPointSize(17)
        font2.setBold(True)
        font2.setWeight(75)
        self.label.setFont(font2)
        self.lblSelectedDirectory = QLabel(self.labeler)
        self.lblSelectedDirectory.setObjectName(u"lblSelectedDirectory")
        self.lblSelectedDirectory.setGeometry(QRect(120, 80, 141, 21))
        self.btnJab = QPushButton(self.labeler)
        self.btnJab.setObjectName(u"btnJab")
        self.btnJab.setGeometry(QRect(800, 70, 81, 31))
        self.btnJab.setStyleSheet(u"background-color: rgba(255, 0, 0, 160); border: none;")
        self.lblSelectedFile = QLabel(self.labeler)
        self.lblSelectedFile.setObjectName(u"lblSelectedFile")
        self.lblSelectedFile.setGeometry(QRect(380, 70, 291, 31))
        font3 = QFont()
        font3.setPointSize(14)
        font3.setBold(False)
        font3.setWeight(50)
        self.lblSelectedFile.setFont(font3)
        self.generateDatasetButton = QPushButton(self.labeler)
        self.generateDatasetButton.setObjectName(u"generateDatasetButton")
        self.generateDatasetButton.setGeometry(QRect(640, 470, 241, 21))
        self.tabWidget.addTab(self.labeler, "")
        self.teach = QWidget()
        self.teach.setObjectName(u"teach")
        self.tabWidget.addTab(self.teach, "")
        self.predict = QWidget()
        self.predict.setObjectName(u"predict")
        self.tabWidget.addTab(self.predict, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 922, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MMA Posture Labeler", None))
        self.import_button.setText(QCoreApplication.translate("MainWindow", u"Import Files", None))
        self.process_button.setText(QCoreApplication.translate("MainWindow", u"Process Files", None))
        self.status_label.setText(QCoreApplication.translate("MainWindow", u"READY", None))

        __sortingEnabled = self.filepaths_list.isSortingEnabled()
        self.filepaths_list.setSortingEnabled(False)
        ___qlistwidgetitem = self.filepaths_list.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"path/fileName", None));
        self.filepaths_list.setSortingEnabled(__sortingEnabled)

        self.clear_button.setText(QCoreApplication.translate("MainWindow", u"Clear List", None))
        self.batch_name_label.setText(QCoreApplication.translate("MainWindow", u"Enter Batch Name", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.openpose), QCoreApplication.translate("MainWindow", u"Keypoint Generator", None))
        self.btnGuard.setText(QCoreApplication.translate("MainWindow", u"Guard", None))
        self.btnSelectDirectory.setText(QCoreApplication.translate("MainWindow", u"Select directory", None))
        self.imagePreview.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Pose labeling", None))
        self.lblSelectedDirectory.setText("")
        self.btnJab.setText(QCoreApplication.translate("MainWindow", u"Jab", None))
        self.lblSelectedFile.setText("")
        self.generateDatasetButton.setText(QCoreApplication.translate("MainWindow", u"Generate dataset from selected frames", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.labeler), QCoreApplication.translate("MainWindow", u"Labeling", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.teach), QCoreApplication.translate("MainWindow", u"Teach", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.predict), QCoreApplication.translate("MainWindow", u"Predict", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
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
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 921, 541))
        self.openpose = QWidget()
        self.openpose.setObjectName(u"openpose")
        self.tabWidget.addTab(self.openpose, "")
        self.labeler = QWidget()
        self.labeler.setObjectName(u"labeler")
        self.tabWidget.addTab(self.labeler, "")
        self.teach = QWidget()
        self.teach.setObjectName(u"teach")
        self.tabWidget.addTab(self.teach, "")
        self.predict = QWidget()
        self.predict.setObjectName(u"predict")
        self.tabWidget.addTab(self.predict, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 922, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.openpose), QCoreApplication.translate("MainWindow", u"Keypoint Generator", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.labeler), QCoreApplication.translate("MainWindow", u"Labeling", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.teach), QCoreApplication.translate("MainWindow", u"Teach", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.predict), QCoreApplication.translate("MainWindow", u"Predict", None))
    # retranslateUi


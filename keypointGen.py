# This Python file uses the following encoding: utf-8
from PySide2.QtWidgets import QFileDialog
import shutil as sh
import os
import cv2
from openpose import OpenPose


class KeyPointGenerator:

    def __init__(self, ui):
        self.ui = ui
        self.files = []
        self.ui.filepaths_list.clear()
        self.ui.openpose_progress.setValue(0)
        self.ui.status_label.setText("Import Files please")
        self.ui.process_button.setEnabled(False)
        print("Keypointgen init")

    def attach(self):
        self.ui.import_button.clicked.connect(self.importButtonClicked)
        self.ui.process_button.clicked.connect(self.processButtonClicked)
        self.ui.clear_button.clicked.connect(self.clearButtonClicked)
        # add list clear btn / also clears self.files

    def clearButtonClicked(self):
        self.ui.status_label.setText("Import Files please")
        self.ui.process_button.setEnabled(False)
        self.ui.filepaths_list.clear()
        self.files = []

    def importButtonClicked(self):
        print("button clicked")

        self.ui.openpose_progress.setValue(0)
        dialog = QFileDialog.getOpenFileNames()
        self.files += dialog[0]

        if len(self.files) > 0:
            for file in dialog[0]:
                splitfilepath = file.split('/')
                self.ui.filepaths_list.addItem(splitfilepath[len(splitfilepath) - 1])
            self.ui.process_button.setEnabled(True)
            self.ui.status_label.setText("READY")

    def processButtonClicked(self):
        self.ui.status_label.setText("PROCESSING")
        if not os.path.exists("temp/"):
            os.mkdir("temp")
        batchName = self.ui.batch_name.toPlainText()
        if len(batchName) <= 0:
            self.ui.status_label.setText("Enter a name for this Batch!")
            return

        dst = "temp/" + batchName + "/"
        if not os.path.exists(dst):
            os.mkdir(dst)
        for src in self.files:
            print(src)
            splitpath = src.split("/")
            sh.copyfile(src, dst + splitpath[len(splitpath) - 1])
        self.keypointgeneration(batchName)

    def keypointgeneration(self, batchName):
        if not os.path.exists("Generated/"):
            os.mkdir("Generated")
        dst = "Generated/" + batchName + "/"
        if not os.path.exists(dst):
            os.mkdir(dst)
        src = "temp/" + batchName + "/"

        # Do Openpose on batch on each video and save keypoints
        i = 0
        progress = 5
        for video in os.listdir(src):
            dumpPath = dst + "Video" + str(i) + "/"
            while os.path.exists(dumpPath):
                i += 1
                dumpPath = dst + "Video" + str(i) + "/"
            os.mkdir(dumpPath)

            vidcap = cv2.VideoCapture(src + video)
            success, image = vidcap.read()
            count = 0
            progress += len(os.listdir(src))
            while success:
                progress += 10 / progress
                self.ui.openpose_progress.setValue(progress)
                cv2.imwrite(dumpPath + "frame%d.jpg" % count, image)  # save frame as JPEG file
                success, image = vidcap.read()
                count += 1
            i += 1
            vidcap.release()

        if os.path.exists(src):
            sh.rmtree(src)

        op = OpenPose()

        for vidBatch in os.listdir(dst):
            progress += 100 / progress
            self.ui.openpose_progress.setValue(progress)
            keypointdst = dst + vidBatch + "/Keypoints"
            if not os.path.exists(keypointdst):
                os.mkdir(keypointdst)

            print("Processing Batch: " + vidBatch)
            op.pose(dst + vidBatch, keypointdst)
            # for each frame Go through openpose and dump output into keypointdst
        self.ui.openpose_progress.setValue(100)
        self.ui.status_label.setText("DONE, You can now close OpenPose window.")

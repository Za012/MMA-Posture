# This Python file uses the following encoding: utf-8

from PySide2.QtWidgets import QFileDialog
from managers.keypoint_manager import KeyPointManager


class KeyPointGenerator:

    def __init__(self, ui):
        self.ui = ui
        self.files = []
        self.keypointsManager = KeyPointManager()
        self.ui.filepaths_list.clear()
        self.ui.openpose_progress.setValue(0)
        self.ui.status_label.setText("Import Files please")
        self.ui.process_button.setEnabled(False)
        print("Keypoint Generator init")

    def attach(self):
        self.ui.import_button.clicked.connect(self.import_button_clicked)
        self.ui.process_button.clicked.connect(self.process_button_clicked)
        self.ui.clear_button.clicked.connect(self.clear_button_clicked)
        # add list clear btn / also clears self.files

    def clear_button_clicked(self):
        self.ui.status_label.setText("Import Files please")
        self.ui.process_button.setEnabled(False)
        self.ui.filepaths_list.clear()
        self.files = []

    def import_button_clicked(self):
        self.ui.openpose_progress.setValue(0)
        dialog = QFileDialog.getOpenFileNames(None, "Select a video", "/", "video(*.mp4 *.avi)")
        self.files += dialog[0]

        if len(self.files) > 0:
            for file in dialog[0]:
                splitfilepath = file.split('/')
                self.ui.filepaths_list.addItem(splitfilepath[len(splitfilepath) - 1])
            self.ui.process_button.setEnabled(True)
            self.ui.status_label.setText("READY")

    def process_button_clicked(self):
        self.ui.status_label.setText("PROCESSING")

        batch_name = self.ui.batch_name.toPlainText()
        if len(batch_name) <= 0:
            self.ui.status_label.setText("Enter a name for this Batch!")
            return

        self.keypointsManager.batchName = batch_name
        self.keypointsManager.create_batch_temporary_directory()

        self.keypointsManager.files = self.files
        self.keypointsManager.copy_files_to_temporary_directory()

        self.keypointsManager.generate_frames_and_keypoints(self.ui.openpose_progress)
        self.ui.status_label.setText("DONE, You can now close OpenPose window.")
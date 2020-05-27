# This Python file uses the following encoding: utf-8


class KeyPointGenerator:

    def __init__(self, ui):
        self.ui = ui
        print("Keypointgen init")

    def attach(self):
        self.ui.import_button.clicked.connect(self.importButtonClicked)

    def importButtonClicked(self):
        print("button clicked")
        self.ui.import_button.setText("False")

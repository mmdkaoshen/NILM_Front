from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


class EnergyLabel(QLabel):
    def __init__(self):
        super().__init__()
        # self.setFixedSize(100, 40)
        self.setText('')
        self.setAlignment(Qt.AlignCenter)

    def changeText(self, text: str):
        self.setText(text)

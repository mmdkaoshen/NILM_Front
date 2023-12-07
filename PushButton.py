from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton


class PushButton(QPushButton):
    def __init__(self, objectName: str):
        super().__init__()
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.setFont(font)
        self.setObjectName(objectName)

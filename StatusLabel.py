from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class StatusLabel(QLabel):
    def __init__(self, icon: str):
        super().__init__()
        self.setFixedSize(100, 100)
        pixmap = QPixmap(icon)
        scaled_pixmap = pixmap.scaled(self.size())
        self.setPixmap(scaled_pixmap)

    def changeIcon(self, icon: str):
        pixmap = QPixmap(icon)
        scaled_pixmap = pixmap.scaled(self.size())
        self.setPixmap(scaled_pixmap)

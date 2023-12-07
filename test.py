import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.add_button = QPushButton("添加控件")
        self.add_button.clicked.connect(self.add_control)
        self.layout.addWidget(self.add_button)

    def add_control(self):
        new_button = QPushButton("新控件")
        self.layout.addWidget(new_button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
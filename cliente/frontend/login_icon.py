from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class LoginIcon(QWidget):
    def __init__(self, name: str = 'X'):
        super().__init__()
        self.name = name
        self.initUI()
        self.close()
        

    def initUI(self):
        self.main_layout = QVBoxLayout()

        self.img = QLabel()
        self.img.setPixmap(QPixmap("Sprites/extra/user_profile.png"))
        self.img.setScaledContents(True)
        self.img.setFixedSize(80, 80)

        self.name_label = QLabel(self.name)
        self.name_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.img)
        self.main_layout.addWidget(self.name_label)

        self.setLayout(self.main_layout)
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from frontend.login_icon import LoginIcon

class Login(QMainWindow):

    signal_start = pyqtSignal()
    signal_exit = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()
        # self.players = [
        #     LoginIcon(name=''),
        #     LoginIcon(name=''),
        #     LoginIcon(name=''),
        #     LoginIcon(name='')
        # ]

    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(0, 0, 800, 600)
        self.setFixedSize(800, 600)
        self.addWidgets()
        self.setStyleSheet(
            "#main {border-image: url(Sprites/background/background_inicio.png);}"
        )
        self.show()
    
    def addWidgets(self):
        self.main = QWidget(self)
        self.main.setObjectName("main")

        self.main_layout = QVBoxLayout()

        self.title = QLabel("SALA DE ESPERA")
        self.title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title)
        self.main_layout.addStretch(2)

        self.players_layout = QHBoxLayout()
        self.players_layout.setAlignment(Qt.AlignCenter)
        self.players_layout.setSpacing(2)
        self.main_layout.addLayout(self.players_layout)
        self.main_layout.addStretch(2)

        self.btn_start = QPushButton("Comenzar")
        self.btn_start.clicked.connect(self.signal_start.emit)
        self.main_layout.addWidget(self.btn_start)

        self.btn_exit = QPushButton("Salir")
        self.btn_exit.clicked.connect(self.signal_exit.emit)
        self.main_layout.addWidget(self.btn_exit)

        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main.setLayout(self.main_layout)
        self.setCentralWidget(self.main)

    def addIcon(self, name: str):
        self.players_layout.addWidget(LoginIcon(name=name))

    # def gameInCourseError(self, message: str):
    #     ...

    # def playerLimitError(self, message: str):
    #     ...
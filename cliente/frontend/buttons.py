
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal, QObject


class Buttons(QObject):

    signal_announce = pyqtSignal(str)
    signal_pass_turn = pyqtSignal()
    signal_change_dice = pyqtSignal()
    signal_use_power = pyqtSignal()
    signal_doubt = pyqtSignal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.initUI()
        self.enabled = False

    def setEnabled(self, _enabled: bool) -> None:
        self.enabled = _enabled
        self.btn_anounce.setEnabled(_enabled)
        self.value.setEnabled(_enabled)
        self.btn_pass.setEnabled(_enabled)
        self.btn_change.setEnabled(_enabled)
        self.btn_use_power.setEnabled(_enabled)
        self.btn_doubt.setEnabled(_enabled)

    def initUI(self) -> None:
        self.ui = QWidget()
        self.layout = QVBoxLayout()

        self.btn_anounce = QPushButton("Anunciar Valor")
        self.value = QLineEdit()
        # self.value.setPlaceholderText("Ingrese valor aqui")

        self.btn_pass = QPushButton("Pasar Turno")
        self.btn_change = QPushButton("Cambiar Dados")
        self.btn_use_power = QPushButton("Usar Poder")
        self.btn_use_power.setEnabled(False)
        self.btn_doubt = QPushButton("Dudar")

        self.btn_anounce.clicked.connect(self.anounce)
        self.btn_pass.clicked.connect(self.signal_pass_turn.emit)
        self.btn_change.clicked.connect(self.signal_change_dice.emit)
        self.btn_use_power.clicked.connect(self.signal_use_power.emit)
        self.btn_doubt.clicked.connect(self.signal_doubt.emit)

        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.btn_anounce)
        self.layout1.addWidget(self.value)
        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.btn_pass)
        self.layout2.addWidget(self.btn_change)
        self.layout3 = QHBoxLayout()
        self.layout3.addWidget(self.btn_use_power)
        self.layout3.addWidget(self.btn_doubt)

        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        self.layout.addLayout(self.layout3)

        self.ui.setLayout(self.layout)

    def anounce(self):
        value = self.value.text()
        # if value.isdigit():
        #     value = int(value)
        # print('>>>>>>', value)
        self.signal_announce.emit(value)


    
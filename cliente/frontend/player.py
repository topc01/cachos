from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel)
from PyQt5.QtGui import QPixmap
from frontend.dice import Dice
from os.path import join, isfile
from os import getcwd
from PyQt5.QtCore import Qt

class Player:
    def __init__(self, name: str = 'X') -> None:
        self._name: str = name
        self.lives = Dice()
        self.lives.setValue(6)
        self.dice1 = Dice()
        self.dice2 = Dice()
        self.initUI()
        
    def initUI(self) -> None:
        self.ui = QWidget()

        self.player_layout = QVBoxLayout()

        self.layout = QHBoxLayout()

        img = QLabel()
        img.setPixmap(QPixmap(join(getcwd(), 'Sprites', 'extra', 'user_profile.png')))
        img.setScaledContents(True)
        img.setFixedSize(80, 80)
        
        self.layout.addWidget(self.lives)
        self.layout.addWidget(img)

        self.name = QLabel(self._name)
        self.name.setAlignment(Qt.AlignCenter)

        self.dices = QHBoxLayout()
        self.dices.addWidget(self.dice1)
        self.dices.addWidget(self.dice2)

        self.player_layout.addLayout(self.layout)
        self.player_layout.addWidget(self.name)
        self.player_layout.addLayout(self.dices)
        self.ui.setLayout(self.player_layout)

    def setLives(self, lives: int) -> None:
        self.lives.setValue(lives)

    def setDices(self, dice1: int, dice2: int) -> None:
        self.dice1.setValue(dice1)
        self.dice2.setValue(dice2)
    
    def setName(self, name: str) -> None:
        self.name.setText(name)

    def see(self) -> None:
        self.dice1.see()
        self.dice2.see()

    def hide(self) -> None:
        self.dice1.hide()
        self.dice2.hide()

    def terminate(self) -> None:
        self.ui.hide()

    def setPlayer(self, lives: int, dice1: int, dice2: int) -> None:
        self.setLives(lives)
        self.setDices(dice1, dice2)
        self.hide()


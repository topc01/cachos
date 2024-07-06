from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QLabel)
from PyQt5.QtCore import Qt
from frontend.player import Player
from frontend.buttons import Buttons
from os.path import join, isfile
from os import getcwd
import time


class UserView(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.players: list[Player] = list()
        self.buttons = Buttons()
        self.buttons.enabled = True
        self.positions = [(0, 1), (1, 0), (2, 1), (1, 2)]

        self.initUI()
        self.hide()

    def initUI(self) -> None:
        self.setWindowTitle("Game")
        self.setGeometry(0, 0, 800, 600)
        self.setFixedSize(800, 600)
        self.addWidgets()
        self.setStyleSheet(
            "#main_widget {border-image: url(Sprites/background/background_juego.png);}"
            # "QWidget {background-color: transparent;}"
        )
        # self.show()

    def addWidgets(self) -> None:
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("main_widget")

        self.main_layout = QVBoxLayout()

        self.player_turn = QLabel()
        # self.player_turn = QLabel("Turno de X")
        self.player_turn.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.player_turn)

        self.stats = QHBoxLayout()
        self.biggest = QLabel()
        # self.biggest = QLabel("Numero mayor anunciado: X")
        self.biggest.setAlignment(Qt.AlignLeft)
        self.last_round = QLabel()
        # self.last_round = QLabel("Turno anterior fue: X")
        self.last_round.setAlignment(Qt.AlignCenter)
        self.round_number = QLabel()
        # self.round_number = QLabel("Numero turno: X")
        self.round_number.setAlignment(Qt.AlignRight)
        self.stats.addWidget(self.biggest)
        self.stats.addWidget(self.last_round)
        self.stats.addWidget(self.round_number)
        self.main_layout.addLayout(self.stats)
        
        self.player_layout = QGridLayout()
        self.player_layout.setSpacing(2)
        self.player_layout.setContentsMargins(0, 0, 0, 0)
        self.player_layout.setColumnStretch(0, 1)
        self.player_layout.setColumnStretch(1, 1)
        self.player_layout.setColumnStretch(2, 1)
        self.player_layout.setRowStretch(0, 1)
        self.player_layout.setRowStretch(1, 1)
        self.player_layout.setRowStretch(2, 1)
        # positions = [(0, 1), (1, 0), (1, 2), (2, 1)]
        # for i, player in enumerate(self.players):
        #     self.player_layout.addWidget(player.ui, *positions[i])

        self.player_layout.addWidget(self.buttons.ui, 2, 2)

        self.main_layout.addLayout(self.player_layout)

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def setLabels(self, current_turn: str, biggest: int, last_round: str, round_number: int) -> None:
        self.player_turn.setText(f"Turno de {current_turn}")
        self.biggest.setText(f"Numero mayor anunciado: {biggest}")
        self.last_round.setText(f"Turno anterior fue: {last_round}")
        self.round_number.setText(f"Numero turno: {round_number}")

    def addPlayer(self, id: int, name: str) -> None:
        pos = self.positions[id]
        player = Player(name)
        self.player_layout.addWidget(player.ui, *pos)
        self.players.append(player)

    def getPlayer(self, id: int) -> Player:
        return self.players[id]
    
    def setPlayer(self, id: int, lives: int, dice1: int, dice2: int) -> None:
        self.players[id].setPlayer(lives, dice1, dice2)

    def seeAll(self) -> None:
        for player in self.players:
            player.see()

    def seePlayer(self, id: int) -> None:
        self.players[id].see()

    def terminatePlayer(self, id: int) -> None:
        self.players[id].terminate()


        
    
    # def hide(self, player: int) -> None:
    #     self.players[player].hide()

    # def testeo_(self) -> None:
    #     time.sleep(7)
    #     self.players[0].setDices(1, 1)
    #     time.sleep(2)
    #     self.players[1].hide()

    
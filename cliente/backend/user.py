from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from frontend.game_ui import UserView
from frontend.login_ui import Login
import json

class User(QObject):

    signal_request = pyqtSignal(str)
    
    def __init__(self, *args, **kwargs) -> None:
        self.id: int
        super().__init__(*args, **kwargs)
        self.loginUI = Login()
        self.gameUI = UserView()
        self.connectSignals()
        self.loginUI.show()

    def handleResponse(self, response: str) -> None:
        response_type, response_data = response.split('$')
        print('[USER] Response received:', response)
        try:
            data: dict = json.loads(response_data)
        except json.decoder.JSONDecodeError:
            print(f'[USER] Error decoding JSON <{response_data}>')
            raise


        if response_type == 'ACCEPT':
            self.id = data['id']

        elif response_type == 'NEW':
            name = data['name']
            self.loginUI.addIcon(name=name)
        
        elif response_type == 'START':
            self.loginUI.close()
            self.gameUI.show()
            for player in data['players']:
                player_id = player['id']
                player_name = player['name']
                self.gameUI.addPlayer(id=player_id, name=player_name)
        
        elif response_type == 'CHANGED':
            self.gameUI.setPlayer(self.id, data['lives'], data['dice1'], data['dice2'])
            self.gameUI.seePlayer(self.id)
            
        elif response_type == 'TURN':
            id = data['id']
            if id == self.id:
                self.gameUI.buttons.setEnabled(True)
            else:
                self.gameUI.buttons.setEnabled(False)
            self.gameUI.setLabels(data['current_player'], data['biggest'], data['last_player'], data['round_number'])
            
        elif response_type == 'ROUND':
            current_turn: str = data['current_player']
            biggest: int = data['biggest']
            last_turn: str = data['last_player']
            round_number: int = data['round_number']
            self.gameUI.setLabels(current_turn, biggest, last_turn, round_number)
            players: list[dict] = data['players']
            for player_data in players:
                player_id = int(player_data['id'])
                player_lives = player_data['lives']
                player_dice1 = player_data['dice1']
                player_dice2 = player_data['dice2']
                self.gameUI.setPlayer(player_id, player_lives, player_dice1, player_dice2)
            self.gameUI.seePlayer(self.id)
            self.gameUI.buttons.setEnabled(False)

        elif response_type == 'SEE':
            self.gameUI.seeAll()

        elif response_type == 'EXIT':
            self.loginUI.close()
            self.gameUI.close()
            exit()

        elif response_type == 'LOST':
            id = data['id']
            name = data['name']
            msg = QMessageBox()
            if id == self.id:
                title = 'Perdiste'
                text = '¡Has perdido una vida!'
                info = 'Dudaron del valor de tus dados'
            else:
                title = f'Jugador {name} perdió'
                text = f'¡{name} ha perdido una vida!'
                info = 'Dudieron del valor de sus dados'
            msg.setWindowTitle(title)
            msg.setText(text)
            msg.setIcon(QMessageBox.Critical)
            msg.setInformativeText(info)
            msg.setStandardButtons(QMessageBox.Abort)
            msg.setDefaultButton(QMessageBox.Abort)
            msg.exec()

        elif response_type == 'REJECT': # TODO: cambiar a REJECT
            error_type = data['type']
            if error_type == 'PLAYING':
                self.gameInCourseError()
            elif error_type == 'FULL':
                self.playerLimitError()
            ...

    def connectSignals(self) -> None:
        self.loginUI.signal_start.connect(self.emit_start)
        self.loginUI.signal_exit.connect(self.emit_exit)

        self.gameUI.buttons.signal_announce.connect(self.announce)
        self.gameUI.buttons.signal_pass_turn.connect(self.passTurn)
        self.gameUI.buttons.signal_change_dice.connect(self.changeDice)
        self.gameUI.buttons.signal_use_power.connect(self.usePower)
        self.gameUI.buttons.signal_doubt.connect(self.doubt)

    def gameInCourseError(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle('Error')
        msg.setText('Partida en juego')
        msg.setIcon(QMessageBox.Critical)
        msg.setInformativeText("Intente más tarde")
        msg.setStandardButtons(QMessageBox.Abort)
        msg.setDefaultButton(QMessageBox.Abort)
        msg.exec()
    
    def playerLimitError(self) -> None:
        msg = QMessageBox()
        msg.setWindowTitle('Error')
        msg.setText('¡SALA LLENA!')
        msg.setIcon(QMessageBox.Critical)
        msg.setInformativeText("Espere un cupo")
        msg.setStandardButtons(QMessageBox.Abort)
        msg.setDefaultButton(QMessageBox.Abort)
        msg.exec()
        ...
        
    def emit_start(self):
        request = 'COMMAND>START$'
        self.signal_request.emit(request)

    def emit_exit(self):
        request = 'COMMAND>EXIT$'
        self.signal_request.emit(request)

    def announce(self, value: str) -> None:
        request = f'PLAY>ANNOUNCE${{"id": {self.id}, "value": {value}}}'
        self.signal_request.emit(request)

    def passTurn(self) -> None:
        request = f'PLAY>PASS${{"id": {self.id}}}'
        self.signal_request.emit(request)

    def changeDice(self) -> None:
        request = f'PLAY>CHANGE${{"id": {self.id}}}'
        self.signal_request.emit(request)
    
    def usePower(self) -> None:
        request = f'PLAY>POWER${{"id": {self.id}}}'
        self.signal_request.emit(request)

    def doubt(self) -> None:
        request = f'PLAY>DOUBT${{"id": {self.id}}}'
        self.signal_request.emit(request)

import sys
import json
import random
from PyQt5.QtCore import QObject
from src.server import Server
import src.utils as utils
from src.user import User, Bot

class MainGame(QObject):
    def __init__(self, port: int) -> None:
        super().__init__()
        self.data = utils.DataFromJSON("./parametros.json")
        self.__host = self.data.HOST
        self.__port = port
        self.server = Server(self.__host, self.__port)
        self.server.cripto = self.data.CRIPTO
        self.setHook()
        self.players : dict[int, User | Bot] = dict()
        self.play = False
        self.__current_player_id = 0
        self.current_round = 0
        self.last_value = 0
        self.last_player_value = 0
        self.last_player_name = '@'
        self.current_player_name = '@'
        self.passed = False
        # self.biggest = 0
    
    @property
    def current_player_id(self):
        return self.__current_player_id
    
    @current_player_id.setter
    def current_player_id(self, value):
        self.__current_player_id = value % self.count

    @property
    def count(self):
        return len(self.players)

    def start(self):
        self.server.signal_request.connect(self.handleRequest)
        self.server.start()
        self.setHook()
        print("[GAME] Running")
        self.cliExit()

    def handleRequest(self, request: str) -> None:
        print('[GAME] Request received:', request)
        request_type, request_data = request.split('>')
        if request_type == 'EVENT':
            self.handleEvent(request_data)
        elif request_type == 'COMMAND':
            self.handleCommand(request_data)
        elif request_type == 'PLAY':
            self.handlePlay(request_data)

    def handleEvent(self, event: str) -> None:
        event_type, event_data = event.split('$')
        data: dict = json.loads(event_data)
        if event_type == 'NEW':
            print('[GAME] New player')
            self.newUser(data)
        elif event_type == 'DISCONNECTED':
            self.disconnectUser(data)
        else:
            print('[GAME] Event not recognized')

    def newUser(self, data: dict) -> None:
        user_id = data['id']
        if self.play:
            response = f'REJECT${{"id": {user_id}, "type": "PLAYING"}}'
            self.sendResponse(response, user_id)
            return
        elif self.count >= self.data.NUMERO_JUGADORES:
            response = f'REJECT${{"id": {user_id}, "type": "FULL"}}'
            self.sendResponse(response, user_id)
            return
        elif user_id in self.players:
            response = f'REJECT${{"id": {user_id}, "type": "REPEATED"}}'
            self.sendResponse(response, user_id)
            return
        user_name = self.data.USER_NAMES[user_id]
        self.players[user_id] = User(user_id, user_name)
        self.sendResponse(f'ACCEPT${{"id": {user_id}}}', user_id)
        print(f'[GAME] Player {user_name} connected with id {user_id}')
        for id, user in self.players.items():
            response = f'NEW${{"name": "{user_name}"}}' # TODO: ver si hay que poner el id
            self.sendResponse(response, id)
            if id != user_id:  # TODO: revisar pq no hay que mandar todos ¿se agrega antes?
                response = f'NEW${{"name": "{user.name}"}}'
                self.sendResponse(response, user_id)

    def disconnectUser(self, data: dict) -> None:
        print(f'[GAME] Player disconnected {data}')
        player_id = data['id']
        self.players.pop(player_id)
        ...

    def handleCommand(self, command: str) -> None:
        command_type, command_data = command.split('$')
        if command_type == 'START':
            self.startGame()
            self.startRound()
        elif command_type == 'EXIT': # TODO: cambiar a END
            self.exitGame()
        elif command_type == 'ROUND':
            self.startRound()
        else:
            print('[GAME] Command not recognized')
    
    def handlePlay(self, play: str) -> None: # TODO last_value se modifica aca
        self.passed = False
        play_type, play_data = play.split('$')
        play_data = json.loads(play_data)
        next: bool
        if play_type == 'ANNOUNCE':
            next = self.announce(play_data)
        elif play_type == 'PASS':
            next = self.passTurn(play_data)
        elif play_type == 'CHANGE':
            next = self.change(play_data)
        elif play_type == 'POWER':
            next = self.power(play_data)
        elif play_type == 'DOUBT':
            next = self.doubt(play_data)
        else:
            print('[GAME] Play not recognized')
        if next: self.main()

    def startGame(self) -> None:
        print('[GAME] Starting game')
        response = 'START$'
        if self.count < self.data.NUMERO_JUGADORES:
            # TODO: agregar bots
            for id in range(self.count, self.data.NUMERO_JUGADORES):
                self.players[id] = Bot(
                    id,
                    self.data.USER_NAMES[id],
                    self.data.PROB_DUDAR,
                    self.data.PROB_ANUNCIAR
                )
        data = {"players": []}
        for id, player in self.players.items():
            data["players"].append({"id": id, "name": player.name})
        response += json.dumps(data)
        self.sendAll(response)
        self.play = True
        # self.round()

    def startRound(self) -> None:
        """
        Inicia una ronda, mandando el estado actual de todos los jugadores
        """
        # se resetean los valores de la ronda
        self.current_round += 1
        self.last_player_name = '@'
        self.current_player_name = self.players[self.current_player_id].name
        self.last_value = 0
        self.passed = False
        for player in self.players.values():
            player.changed = False

        print(f'[GAME] Starting round {self.current_round}')
        self.throwDices()

        data = self.getStatus() # current_turn, biggest, last_player, round_number
        players_data = self.getPlayers() # id, lives, dice1, dice2 de cada jugador
        data['players'] = players_data
        response = 'ROUND$' + json.dumps(data)
        self.sendAll(response)
        self.main()

    def main(self) -> None:
        """
        Loop principal del turno
        """
        for player in self.players.values():
            player.changed = False
        id = self.current_player_id
        response = f'TURN$'
        data = {
            "id": id,
            "current_player": self.current_player_name,
            "biggest": self.last_value,
            "last_player": self.last_player_name,
            "round_number": self.current_round
        }
        response += json.dumps(data)
        self.sendAll(response)
        if isinstance(self.players[id], Bot):
            dices = (random.randint(1, 6), random.randint(1, 6))
            play = self.players[id].play(self.last_value, dices)
            self.handlePlay(play)
        self.last_player_value = self.players[id].value
        self.current_player_id += 1
        self.last_player_name = self.current_player_name
        self.current_player_name = self.players[self.current_player_id].name

    def nextTurn(self) -> None:
        """
        Cambia el turno al siguiente jugador
        """
        while not self.endRound():
            ...
            self.current_player_id += 1

    def endRound(self) -> bool:
        """
        Verifica si la ronda terminó
        """

    def announce(self, data: dict) -> None:
        id = data['id']
        value: str = data['value']
        if not str(value).isdigit():
            return False
        value = int(value)
        current_player = self.players[id]
        print(f'[GAME] Player {current_player.name} announced {value}')
        if value <= self.last_value:
            print(f'[GAME] Player {current_player.name} invalid announcement')
            return False
        self.last_value = value
        return True

    def passTurn(self, data: dict) -> None:
        id = data['id']
        current_player = self.players[id]
        print(f'[GAME] Player {current_player.name} passed')
        self.passed = True
        return True
    
    def change(self, data: dict) -> None: # TODO SE ESCONDEN LOS DADOS
        id = data['id']
        current_player = self.players[id]
        if not current_player.changed:
            print(f'[GAME] Player {current_player.name} changed dices')
            current_player.changed = True
            current_player.dice1 = random.randint(1, 6)
            current_player.dice2 = random.randint(1, 6)
            response = 'CHANGED$' + json.dumps({
                "lives": current_player.lives,
                "dice1": current_player.dice1,
                "dice2": current_player.dice2
            })
            self.sendResponse(response, id)
            return True
        return False

    def doubt(self, data: dict) -> None:
        id = data['id']
        print(f'[GAME] Player {self.players[id].name} doubted')
        response = 'SEE$'
        self.sendAll(response)
        
        if self.passed:
            value = self.data.VALOR_PASO
        else:
            value = self.last_value

        if self.last_player_value != value:
            self.current_player_id -= 1
            self.players[self.current_player_id].lives -= 1
            name = self.players[self.current_player_id].name
        else:
            self.players[id].lives -= 1
            name = self.players[id].name
        print(f'[GAME] Player {name} lost a life')
        response = 'LOST$' + json.dumps({"id": id, "name": name})
        self.sendAll(response)
        self.startRound()
        return False
            

    def throwDices(self) -> None: 
        for _, player in self.players.items():
            player.dice1 = random.randint(1, 6)
            player.dice2 = random.randint(1, 6)

    def getPlayers(self) -> list:
        player_data = []
        for id, player in self.players.items():
            player_data.append({
                "id": id,
                "lives": player.lives,
                "dice1": player.dice1,
                "dice2": player.dice2
            })
        return player_data

    def getStatus(self) -> dict:
        return {
            "current_player": self.current_player_name,
            "biggest": self.last_value,
            "last_player": self.last_player_name,
            "round_number": self.current_round,
        }
    
    def sendAll(self, response: str) -> None:
        for id, player in self.players.items():
            if isinstance(player, Bot):
                continue
            self.sendResponse(response, id)

    def sendResponse(self, response: str, id: int) -> None:
        self.server.send(response, id)

    def cliExit(self):
        """command line interface to exit the game"""
        input()
        self.exitGame()
    
    def exitGame(self):
        print("[MAIN] Exiting")
        self.server.end()
        exit()

    def setHook(self):
        def hook(type, value, traceback):
            print(type)
            print(traceback)
        sys.__excepthook__ = hook

import random

class User:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.lives = 6
        self.dice1 = 0
        self.dice2 = 0
        self.changed = False
    
    @property
    def value(self) -> int:
        return self.dice1 + self.dice2
    
    def getState(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'lives': self.lives,
            'dice1': self.dice1,
            'dice2': self.dice2
        }
    
    def setState(self, state: dict) -> None:
        self.lives = state['lives']
        self.dice1 = state['dice1']
        self.dice2 = state['dice2']

class Bot(User):
    def __init__(self, id: int, name: str, prob_doubt: float, prob_play: float) -> None:
        super().__init__(id, name)
        self.PROB_DOUBT = prob_doubt
        self.PROB_PLAY = prob_play
        self.PROB_PASS = 1 - self.PROB_DOUBT - self.PROB_PLAY
    
    def play(self, previous_play: int, dices: tuple[int, int]) -> str:
        jugada = random.random()
        if jugada < self.PROB_DOUBT:
            return f'DOUBT${{"id": {self.id}}}'
        self.dice1, self.dice2 = dices
        if jugada < self.PROB_DOUBT + self.PROB_PLAY and previous_play < 12:
            value = random.randint(previous_play+1, 12)
            if value != 12:
                return f'ANNOUNCE${{"id": {self.id}, "value": {value}}}'
        return f'PASS${{"id": {self.id}}}'
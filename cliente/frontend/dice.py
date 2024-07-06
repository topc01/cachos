from os.path import join, isfile
from os import getcwd
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QStackedLayout, QStackedWidget, QWidget, QLabel)

class Dice(QLabel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.initUI()
        self.value: int = 0
        self.setImg(0)
        
    def setValue(self, value: int) -> None:
        self.value = value
        self.setImg(value)
    
    def setImg(self, value: int) -> None:
        self.setPixmap(self.imgs[value])
        self.setScaledContents(True)

    def initUI(self) -> None:
        self.imgs = [
            QPixmap(join(getcwd(), 'Sprites', 'dices', 'dice_background.png')),
            QPixmap(join(getcwd(), 'Sprites', 'dices', 'dice_1.png')),
            QPixmap(join(getcwd(), 'Sprites', 'dices', 'dice_2.png')),
            QPixmap(join(getcwd(), 'Sprites', 'dices', 'dice_3.png')),
            QPixmap(join(getcwd(), 'Sprites', 'dices', 'dice_4.png')),
            QPixmap(join(getcwd(), 'Sprites', 'dices', 'dice_5.png')),
            QPixmap(join(getcwd(), 'Sprites', 'dices', 'dice_6.png')),
        ]
        self.setFixedSize(50, 50)
    
    def see(self) -> None:
        self.setImg(self.value)

    def hide(self) -> None:
        self.setImg(0)

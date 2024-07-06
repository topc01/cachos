import sys
import threading
from PyQt5.QtWidgets import QApplication
from src.server import Server
from src.game import MainGame
import src.utils as utils
# from src.app import 


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 9994
        print(f"[MAIN] No port specified, using {port}")
    app = QApplication([])
    mainGame = MainGame(port)
    mainGame.start()
    print("[MAIN] Started")
    sys.exit(app.exec())

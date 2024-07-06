import sys
from PyQt5.QtWidgets import QApplication
from backend.client import Client
import backend.utils as utils
from backend.user import User
# from frontend.game_window import UserView


class App(QApplication):
    def __init__(self):
        super().__init__([])

        def hook(type, value, traceback):
            print(type)
            print(traceback)
        sys.__excepthook__ = hook

        # self.index = 0
        self.initBackend()
        self.initFrontend()
        self.client.start()
        self.connect()
        # self.user.start()
        
    def initBackend(self):
        self.client = Client(host, port)
        self.client.cripto = data.CRIPTO
        self.user = User()

    def initFrontend(self):
        ...
        # self.game_window = UserView()

    def connect(self):
        self.client.signal_response.connect(self.user.handleResponse)
        self.user.signal_request.connect(self.client.send)

    def run(self):
        sys.exit(self.exec())

    def close(self):
        # self.game_window.close()
        self.user.close()
        self.exit(0)


def main():
    app = App()
    app.run()

def finish():
    pass

if __name__ == "__main__":
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        print("Usage: python3 main.py [port]")
        print("Default port: 9000")
        port = 9000

    data = utils.DataFromJSON("parametros.json")
    host = data.HOST

    try:
        main()
    except KeyboardInterrupt:
        print("\[CLIENT] stopped")
        finish()
    

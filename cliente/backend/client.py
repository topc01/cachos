import socket
import threading
import backend.utils as utils
from PyQt5.QtCore import pyqtSignal, QObject
class Client(QObject):

    signal_response = pyqtSignal(str)

    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self.host : str = host
        self.port : int = port
        self.cripto = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_server_thread = threading.Thread(target=self.listen, daemon=True)

    def start(self):
        try:
            self.socket.connect((self.host, self.port))
        except ConnectionRefusedError:
            print(f"[CLIENT] Server not running in {self.host}:{self.port}")
            exit()
        self.listen_server_thread.start()

    def listen(self):
        while utils.isReadable(self.socket):
            try:
                recieved_length_bytes = self.socket.recv(4)
            except ConnectionResetError:
                print(f"[CLIENT] Connection reseted")
                exit()
            recieved_length = int.from_bytes(
                recieved_length_bytes,
                byteorder='little'
            )
            recieved = bytearray()

            while len(recieved) < recieved_length:
                read_length = min(4096, recieved_length - len(recieved))
                recieved.extend(self.socket.recv(read_length))
            
            if self.cripto:
                command = utils.decode(recieved)
                print('>>>>>>>>>>', command, recieved.decode(encoding='utf-8'))
            else:
                command = recieved.decode(encoding='utf-8')
            # print(command, command2)
            # if not command == command2:
            #     print("ERROR")
            print(f"[CLIENT] Command recieved: {command}")

            if command != "":
                self.signal_response.emit(command)

    def send(self, message: str):
        message = str(message)
        if self.cripto:
            msg_bytes = utils.encode(message)
        else:
            msg_bytes = message.encode(encoding='utf-8')
        msg_length = len(msg_bytes).to_bytes(4, byteorder='little')
        self.socket.sendall(msg_length + msg_bytes)

if __name__ == "__main__":
    host = socket.gethostname()
    port = 9994
    server = Client(host, port)
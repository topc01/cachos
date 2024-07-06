import socket
import threading
import src.utils as utils
from PyQt5.QtCore import QObject, pyqtSignal

class Server(QObject):

    signal_request = pyqtSignal(str)

    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        # self.id = 0
        self.host : str = host
        self.port : int = port
        self.counter = 0
        self.cripto = True
        self.sockets : dict[int, socket.socket] = dict()
        self.running = True
        self.connect_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.connection_thread = threading.Thread(target=self.acceptConnections, daemon=True)
        self.connection_thread = threading.Thread(target=self.acceptConnections)
        print(f"[SERVER] Server created in {self.host}:{self.port}")

    def start(self):
        self.connect_skt.bind((self.host, self.port))
        self.connect_skt.listen()
        print(f"[SERVER] Listening in {self.host}:{self.port}")
        self.connection_thread.start()


    def acceptConnections(self) -> None:
        while self.running:
            # print("[SERVER] Waiting for connections")
            # client_skt, addres = self.connect_skt.accept()
            try:
                client_skt, addres = self.connect_skt.accept()
            except ConnectionAbortedError:
                print(f"[SERVER] Connection aborted")
                exit()
            except OSError:
                print(f"[SERVER] Connection closed")
                exit()
            
            print(f"[SERVER] Connecting client from {addres}")
            if not utils.isReadable(client_skt):
                print(f"[SERVER] Connection to {addres} failed")
                continue
            skt_id = self.counter
            self.sockets[skt_id] = client_skt
            listen_client_thread = threading.Thread(target=self.listenClient, args=(skt_id, ))
            listen_client_thread.start()
            self.counter += 1
            request = f'EVENT>NEW${{"id": {skt_id}}}'
            self.signal_request.emit(request)
            print(f"[SERVER] Request {request} sent to game")
    
    def listenClient(self, socket_id: int) -> None:
        client_socket: socket.socket = self.sockets[socket_id]
        while self.running and utils.isReadable(client_socket):
            try:
                recieved_length_bytes = client_socket.recv(4)
            except ConnectionAbortedError:
                print(f"[SERVER] Connection aborted")
                break
            except Exception as e:
                print(f"[SERVER] Exception {e}")
                break
            recieved_length = int.from_bytes(
                recieved_length_bytes, byteorder='little'
            )
            recieved = bytearray()

            while len(recieved) < recieved_length:
                read_length = min(4096, recieved_length - len(recieved))
                recieved.extend(client_socket.recv(read_length))
            
            if self.cripto:
                request = utils.decode(recieved)
            else:
                request = recieved.decode(encoding='utf-8')

            if request != "":
                self.signal_request.emit(request)

        print(f"[SERVER] Client {socket_id} disconnected")
        request = f'EVENT>DISCONNECTED${{"id": {socket_id}}}'
        self.signal_request.emit(request)

    def send(self, message: str, skt_id: int) -> None:
        if skt_id == -1:
            self.sendAll(message)
            return
        socket_ = self.sockets[skt_id]
        if not utils.isReadable(socket_):
            return
        message = str(message)
        print(f"[SERVER] Sending {message} to {skt_id}")
        if self.cripto:
            msg_bytes = utils.encode(message)
        else:
            msg_bytes = message.encode(encoding='utf-8')
        msg_length = len(msg_bytes).to_bytes(4, byteorder='little')
        socket_.sendall(msg_length + msg_bytes)
    
    def end(self):
        # print(1.1)
        self.running = False
        # print(1.2)
        # print(1.3)
        for skt_id, skt in self.sockets.items():
            skt: socket.socket
            self.send('EXIT${}', skt_id)
            skt.close()
        self.connect_skt.close()
        print("[SERVER] Stopped")

    def sendAll(self, message: str) -> None:
        for skt_id in self.sockets:
            self.send(message, skt_id)

if __name__ == "__main__":
    host = socket.gethostname()
    port = 9994
    server = Server(host, port)
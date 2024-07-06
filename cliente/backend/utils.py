import typing
from typing import Any
import socket
import json
import os
from Scripts.cripto import encriptar, desencriptar


def isReadable(sock: socket.socket) -> bool:
    try:
    # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return False
    except BlockingIOError:
        return True  # socket is open and reading from it would block
    except ConnectionResetError:
        return False  # socket was closed for some other reason
    except IOError:
        return False # socket was closed
    return True

class DataFromJSON:
    def __init__(self, filename: str) -> None:
        if not os.path.isfile(filename):
            raise FileNotFoundError("File not found")
        with open(filename, "r") as file:
            self.data : dict = json.load(file)
        
    def __getattr__(self, __name: str) -> int | str | list:
        return self.data.get(__name.lower()) or self.data.get(__name.upper())

def encode(msg: str) -> bytearray:
    encoded_msg = bytearray()

    bytes_msg = msg.encode(encoding='utf-8')
    if len(msg) != len(bytes_msg):
        raise ValueError("Length of message and bytes message are not equal")
    
    chunks_amount = len(bytes_msg) // 128 + 1
    for i in range(chunks_amount):
        index = i.to_bytes(4, byteorder='big')
        inital = i * 128
        final = min((i + 1) * 128, len(bytes_msg))
        chunk = bytes_msg[inital:final]
        if len(chunk) < 128:
            chunk += b'\x00' * (128 - len(chunk))
        encoded_msg.extend(index + chunk)
    
    return encoded_msg

def decode(msg: bytearray) -> str:
    chunks: list[tuple[int, str]] = list()
    
    index = 0
    while index < len(msg):
        chunk_index = int.from_bytes(msg[index:index + 4], byteorder='big')
        chunk = msg[index + 4:index + 132]
        chunks.append((chunk_index, chunk.decode(encoding='utf-8')))
        index += 132

    decoded_msg = str()
    for chunk in sorted(chunks, key=lambda x: x[0]):
        decoded_msg += chunk[1]

    return decoded_msg
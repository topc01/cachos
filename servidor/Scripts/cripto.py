def encriptar(msg: bytearray, N: int) -> bytearray:
    l = len(msg)
    new = bytearray(l)
    for i, byte in enumerate(msg):
        new[(i + N) % l] = byte
    new[0], new[N] = new[N], new[0]
    return new

def desencriptar(msg: bytearray, N: int) -> bytearray:
    l = len(msg)
    new = bytearray(l)
    msg[0], msg[N] = msg[N], msg[0]
    for i, _ in enumerate(msg):
        new[i] = msg[(i + N) % l]
    return new
    
if __name__ == "__main__":
    # Testear encriptar
    N = 1
    msg_original = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04\x05')
    msg_esperado = bytearray(b'\x01\x05\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04')
    msg_encriptado = encriptar(msg_original, N)
    # print(msg_encriptado)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")
    
    # Testear desencriptar
    msg_desencriptado = desencriptar(msg_esperado, N)
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")
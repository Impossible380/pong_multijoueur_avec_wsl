def send_number(sock, number):
    sock.send(number.to_bytes(4, "big"))


def send_key(sock, key):
    sock.send("key".encode())
    send_number(sock, key)


def send_position(sock, x, y):
    sock.send("pos".encode())
    send_number(sock, x)
    send_number(sock, y)


def send_string(sock, character_string):
    sock.send("str".encode())
    send_number(sock, len(character_string))
    sock.send(character_string.encode())


def read_number(sock):
    return int.from_bytes(sock.recv(4), "big")


def read_packet(sock: str):
    type = sock.recv(3).decode()
    if type == "key":
        key = read_number(sock)
        return {"type": type, "data": key}
    elif type == "pos":
        x = read_number(sock)
        y = read_number(sock)
        return {"type": type, "data": (x, y)}
    else:
        length_character_string = read_number(sock)
        character_string = sock.recv(length_character_string).decode()
        return {"type": type, "data": character_string}




# Netsh wlan show profile name="Livebox-6399" key=clear
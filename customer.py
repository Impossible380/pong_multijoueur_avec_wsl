#!/usr/bin/python3


from click import getchar
from functions import *
from pong_terminal import *
import socket
import sys
import threading


# Routine d'envoi
def handle_send(myself):
    global is_playing

    print(f"Hello {myself['name']}, welcome to pong !")

    while is_playing:
        char = getchar(echo=False)

        if char == "z" or char == "s":
            key_int = 0 if char == "z" else 1

            send_key(myself["socket"], key_int)


# Connexion au serveur
server = ("172.24.193.202", 8080)

# AF_INET (address family) : on utiliuse l'ipv4
# SOCK_STREAM : Transmission Control Protocol (TCP)


# Mon initialisation

# Mon socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setblocking(True)
sock.connect(server)

# Mon id
id = read_number(sock)

# Mon nom
name = input("What's your name ? ") if len(sys.argv) < 2 else sys.argv[1]
send_string(sock, name)

# Mes informations
myself = {"id": id, "name": name, "socket": sock}


# La partie va bientôt débuter
is_playing = True

packet = read_packet(myself["socket"])
game_start = packet["data"]
print(game_start)

# Début du thread d'envoi
thread_send = threading.Thread(target=handle_send, args=(myself,))
thread_send.start()


# Initialisation des entités
erase_screen()
hide_cursor()

ball = {"color": "yellow", "position": (60, 14)}
print_ball(*ball["position"])

racket_1 = {"color": "blue", "position": (30, 14)}
print_racket(racket_1["color"], *racket_1["position"])

racket_2 = {"color": "red", "position": (90, 14)}
print_racket(racket_2["color"], *racket_2["position"])


# Routine de réception
while is_playing:
    color_packet = read_packet(myself["socket"])
    color = color_packet["data"]
    position_packet = read_packet(myself["socket"])

    if position_packet["type"] == "pos":
        if color == ball["color"]:
            erase_ball(*ball["position"])
            ball["position"] = position_packet["data"]
            print_ball(*ball["position"])

        else:
            racket = racket_1 if color == racket_1["color"] else racket_2
            
            erase_racket(*racket["position"])
            racket["position"] = position_packet["data"]
            print_racket(racket["color"], *racket["position"])
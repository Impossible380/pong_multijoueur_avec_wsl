#!/usr/bin/python3


from functions import *
from game import *
import socket
import threading
import time


# Routine de réception
def handle_receive(player, log_level=0):
    global is_playing
    global key_int
    global last_player

    while is_playing:
        packet = read_packet(player["socket"])
        if log_level == 1:
            print(f"[LOG]: Received: {packet} by {player['name']}")

        if packet["type"] == "key":
            key_int = packet["data"]
            last_player = player


IP = "172.24.193.202"
PORT = 8080

server = socket.create_server((IP, PORT))

is_playing = True
key_int = 2
last_player = {}

players = []
id = 0

game = Game(120, 24, players)

while len(players) < 2:
    id += 1

    # Socket du joueur
    server.listen()
    sock, address = server.accept()
    sock.setblocking(True)

    # Id du joueur
    send_number(sock, id)

    # Nom du joueur
    packet = read_packet(sock)
    name = packet["data"]

    # Intégration du joueur dans la liste des joueurs
    player = {"id": id, "name": name, "socket": sock}
    players.append(player)
    print(f"{player['name']} arrived ! {len(players)}/2")

    # Début du thread de réception
    thread_read = threading.Thread(target=handle_receive, args=(player, 1))
    thread_read.start()

# La partie va bientôt débuter
for player in players:
    send_string(player["socket"], "BEGIN")


"""   Début Game   """
x_move_ball = 2
y_move_ball = 1

time.sleep(1)
# Routine d'envoi
while is_playing:
    # Mouvement de la balle
    x_move_ball, y_move_ball = game.move_ball(x_move_ball, y_move_ball)

    if key_int == 0:
        game.move_racket(last_player["id"], -1)
        key_int = 2

    if key_int == 1:
        game.move_racket(last_player["id"], 1)
        key_int = 2

    for player in players:
        # Envoi de la position de la balle
        send_string(player["socket"], game.ball.color)
        send_position(player["socket"], *game.ball.position)

        # Envoi de la position des raquettes
        send_string(player["socket"], game.racket_1.color)
        send_position(player["socket"], *game.racket_1.position)

        send_string(player["socket"], game.racket_2.color)
        send_position(player["socket"], *game.racket_2.position)
    
    time.sleep(0.1)
"""   Fin Game   """
#!/usr/bin/python3


from functions import *
from game import *
import os
import signal
import socket
import threading
import time


def sigint_handler(signum, frame):
    print(" Exiting...")
    os._exit(0)


# Routine de réception
def handle_receive(player, log_level=0):
    global is_playing

    while is_playing:
        packet = read_packet(player["socket"])
        if log_level == 1:
            print(f"[LOG]: Received: {packet} by {player['name']}")

        if packet["type"] == "key":
            player["has_moved"] = -1 if packet["data"] == 2 else 1


signal.signal(signal.SIGINT, sigint_handler)

# Création du serveur
IP = "172.24.193.202"
PORT = 8080

server = socket.create_server((IP, PORT))


# Initialisation des joueurs
players = []
id = 0

while len(players) < 2:
    id += 1

    # Socket du joueur
    server.listen()
    sock, address = server.accept()

    # Id du joueur
    send_number(sock, id)

    # Nom du joueur
    packet = read_packet(sock)
    name = packet["data"]

    # Intégration du joueur dans la liste des joueurs
    player = {"id": id, "name": name, "socket": sock}
    players.append(player)
    print(f"{player['name']} est arrivé ! {len(players)}/2")


# Préparation
is_playing = True

for player in players:
    send_string(player["socket"], "C'est parti !")

    player["score"] = 0
    player["has_moved"] = 0

    # Début du thread de réception
    player["thread"] = threading.Thread(target=handle_receive, args=(player, 1))
    player["thread"].start()


"""   Début Game   """
game = Game(players)

x_move_ball = 3
y_move_ball = 1

time.sleep(1)
# Routine d'envoi
while is_playing:
    # Mouvement de la balle
    x_move_ball, y_move_ball = game.move_ball(x_move_ball, y_move_ball)
    
    entities = [game.ball, game.racket_1, game.racket_2]

    for player in game.players:
        if player["has_moved"]:
            game.move_racket(player["id"], player["has_moved"] * 2)
            player["has_moved"] = 0

        # Envoi de la position de la balle et des raquettes
        for entity in entities:
            send_string(player["socket"], entity.color)
            send_position(player["socket"], *entity.position)

        # Envoi des scores
        send_number(player["socket"], game.players[0]["score"])
        send_number(player["socket"], game.players[1]["score"])
    
    if game.players[0]["score"] >= 3 or game.players[1]["score"] >= 3:
        break
    
is_playing = False

print(is_playing)

for player in players:
    player["thread"].join()
"""   Fin Game   """
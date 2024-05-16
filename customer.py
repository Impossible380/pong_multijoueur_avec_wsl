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
            key_int = 2 if char == "z" else 1

            send_key(myself["socket"], key_int)


# Connexion au serveur
server = ("172.24.193.202", 8080)

# AF_INET (address family) : on utiliuse l'ipv4
# SOCK_STREAM : Transmission Control Protocol (TCP)


# Mon initialisation

# Mon socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

print_wall()

ball = {"color": "yellow", "position": (60, 14)}
print_ball(*ball["position"])

ball = {"color": "yellow", "position": (60, 14)}
print_ball(*ball["position"])

racket_1 = {"color": "blue", "position": (20, 14)}
print_racket(racket_1["color"], *racket_1["position"])

racket_2 = {"color": "red", "position": (100, 14)}
print_racket(racket_2["color"], *racket_2["position"])


number_packet = 0
# Routine de réception
while is_playing:
    number_packet += 1

    if number_packet != 4:
        c_packet = read_packet(myself["socket"])
        color = c_packet["data"]
        
        packet = read_packet(myself["socket"])

        if packet["type"] == "pos":
            if color == ball["color"]:
                erase_ball(*ball["position"])
                ball["position"] = packet["data"]
                print_ball(*ball["position"])

            else:
                racket = racket_1 if color == racket_1["color"] else racket_2
                
                erase_racket(*racket["position"])
                racket["position"] = packet["data"]
                print_racket(racket["color"], *racket["position"])
    
    else:
        score_1 = read_number(myself["socket"])
        score_2 = read_number(myself["socket"])

        print_message(30, score_1)
        print_message(90, score_2)

        if myself["id"] == 1:
            my_score = score_1
            opponent_score = score_2
        else:
            my_score = score_2
            opponent_score = score_1
        
        if my_score >= 3:
            print_message(48, f"Bravo, vous avez gagné !")
            break
        elif opponent_score >= 3:
            print_message(48, f"Dommage, vous avez perdu !")
            break
        
        number_packet = 0

is_playing = False
thread_send.join()
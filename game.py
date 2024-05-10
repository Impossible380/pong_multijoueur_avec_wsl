from pong_terminal import *
import time


class Game:
    def __init__(self, players):
        self.players = players
        self.screen = (120, 24)

        self.ball_default_position = (60, 14)
        self.racket_1_default_position = (30, 14)
        self.racket_2_default_position = (90, 14)

        self.ball = Entity("yellow", self.ball_default_position)
        self.racket_1 = Entity("blue", self.racket_1_default_position)
        self.racket_2 = Entity("red", self.racket_2_default_position)
    
    def ball_touch_wall(self, axis, axis_move_ball):
        if axis == 0:
            if self.ball.position[0] + 1 >= self.screen[0]:
                self.players[0]["score"] += 1

                self.ball.position = list(self.ball_default_position)
                self.racket_1.position = list(self.racket_1_default_position)
                self.racket_2.position = list(self.racket_2_default_position)
                axis_move_ball = -axis_move_ball
                time.sleep(1)
            
            elif self.ball.position[0] <= 0:
                self.players[1]["score"] += 1

                self.ball.position = list(self.ball_default_position)
                self.racket_1.position = list(self.racket_1_default_position)
                self.racket_2.position = list(self.racket_2_default_position)
                axis_move_ball = -axis_move_ball
                time.sleep(1)
        
        else:
            if self.ball.position[1] <= 4 or \
                    self.ball.position[1] >= self.screen[1]:
                self.ball.position[1] -= axis_move_ball
                axis_move_ball = -axis_move_ball
        
        return axis_move_ball
    
    def ball_touch_racket(self, x_move_ball, y_move_ball, player_id):
        racket = self.racket_1 if player_id == 1 else self.racket_2

        if self.ball.position[0] + 2 >= racket.position[0] and \
                self.ball.position[0] - 1 <= racket.position[0] and \
                self.ball.position[1] + 1 >= racket.position[1] - 2 and \
                self.ball.position[1] - 1 <= racket.position[1] + 2:
            
            if self.ball.position[0] + 1 <= racket.position[0] or \
                    self.ball.position[0] >= racket.position[0]:
                self.ball.position[0] -= x_move_ball
                x_move_ball = -x_move_ball
            
            if self.ball.position[1] + 1 <= racket.position[1] - 2 or \
                    self.ball.position[1] - 1 >= racket.position[1] + 2:
                self.ball.position[1] -= y_move_ball
                y_move_ball = -y_move_ball

        return x_move_ball, y_move_ball

    def move_ball(self, x_move_ball, y_move_ball):
        self.ball.position[0] += x_move_ball
        self.ball.position[1] += y_move_ball

        x_move_ball = self.ball_touch_wall(0, x_move_ball)
        y_move_ball = self.ball_touch_wall(1, y_move_ball)

        for player in self.players:
            x_move_ball, y_move_ball = self.ball_touch_racket(x_move_ball, y_move_ball, player["id"])
        
        return x_move_ball, y_move_ball
    
    def move_racket(self, id, y_move_racket):
        racket = self.racket_1 if id == 1 else self.racket_2

        racket.position[1] += y_move_racket

        if racket.position[1] < 2 or racket.position[1] > self.screen[1] - 2:
            racket.position[1] -= y_move_racket


class Entity:
    def __init__(self, color, position):
        self.color = color
        self.position = list(position)


if __name__ == "__main__":
    players = [{"name": "Dif_269"}, {"name": "Imp_369"}]

    is_playing = True


    # Test unitaire du module 'game.py'
    """   Début Game   """
    game = Game(players)

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
        
        # print(f"{game.players[0]['points']} - {game.players[1]['points']}")

        print_score(game.players[0]["score"], 30)
        print_score(game.players[1]["score"], 90)
        
        if game.players[0]["score"] >= 3:
            print(f"Victoire de {game.players[0]['name']}")
            is_playing = False
        elif game.players[1]["score"] >= 3:
            print(f"Victoire de {game.players[1]['name']}")
            is_playing = False
        
        time.sleep(0.1)
    """   Fin Game   """
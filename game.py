from pong_terminal import *


class Game:
    def __init__(self, width, height, players):
        self.screen = (width, height)
        self.players = players

        self.ball = Ball("yellow", (60, 12))

        self.racket_1 = Racket("blue", (30, 12))
        self.racket_2 = Racket("red", (90, 12))
    
    def ball_collision(self, axis, axis_move_ball, first_point, last_point):
        axis = int(axis)

        if self.ball.position[axis] <= first_point[axis] or \
                self.ball.position[axis] >= last_point[axis]:
            self.ball.position[axis] -= axis_move_ball
            return -axis_move_ball
        
        else:
            return axis_move_ball

    def move_ball(self, x_move_ball, y_move_ball):
        self.ball.position[0] += x_move_ball
        self.ball.position[1] += y_move_ball

        x_move_ball = self.ball_collision(0, x_move_ball, (0, 0), self.screen)
        y_move_ball = self.ball_collision(1, y_move_ball, (0, 0), self.screen)

        x_move_ball = self.ball_collision(0, x_move_ball, self.racket_1.position,
                                          self.racket_1.position)
        y_move_ball = self.ball_collision(1, y_move_ball, self.racket_1.position - 2,
                                          self.racket_1.position + 2)

        x_move_ball = self.ball_collision(0, x_move_ball, self.racket_2.position,
                                          self.racket_2.position)
        y_move_ball = self.ball_collision(1, y_move_ball, self.racket_2.position - 2,
                                          self.racket_2.position + 2)

        """ if self.ball.position[0] <= 0 or self.ball.position[0] >= self.width:
            x_move_ball = -x_move_ball
            self.ball.position[0] += x_move_ball
        
        if self.ball.position[1] <= 0 or self.ball.position[1] >= self.height:
            y_move_ball = -y_move_ball
            self.ball.position[1] += y_move_ball
        
        if self.ball.position[0] >= self.racket_1.position[0] and \
                self.ball.position[0] <= self.racket_1.position[0]:
            x_move_ball = -x_move_ball
            self.ball.position[1] += x_move_ball
        
        if self.ball.position[1] >= self.racket_1.position[1] and \
                self.ball.position[1] <= self.racket_1.position[1]:
            y_move_ball = -y_move_ball
            self.ball.position[1] += y_move_ball
        
        if self.ball.position[0] >= self.racket_2.position[0] and \
                self.ball.position[0] <= self.racket_2.position[0]:
            x_move_ball = -x_move_ball
            self.ball.position[1] += x_move_ball
        
        if self.ball.position[1] >= self.racket_2.position[1] and \
                self.ball.position[1] <= self.racket_2.position[1]:
            y_move_ball = -y_move_ball
            self.ball.position[1] += y_move_ball """

        
        return x_move_ball, y_move_ball
    
    def move_racket(self, id, y_move_racket):
        racket = self.racket_1 if id == 1 else self.racket_2

        racket.position[1] += y_move_racket

        if racket.position[1] < 2 or racket.position[1] > self.height - 2:
            racket.position[1] -= y_move_racket


class Ball:
    def __init__(self, color, position):
        self.color = color
        self.position = list(position)


class Racket:
    def __init__(self, color, position):
        self.color = color
        self.position = list(position)


if __name__ == "__main__":
    players = [{"name": "Dif_269"}, {"name": "Imp_369"}]

    game = Game(120, 24, players)
    is_playing = True


    # Test unitaire du module 'game.py'
    """   Début Game   """
    x_move_ball = 2
    y_move_ball = 1

    time.sleep(1)
    # Routine d'envoi
    while is_playing:
        # Mouvement de la balle
        x_move_ball, y_move_ball = game.move_ball(x_move_ball, y_move_ball)

        if key_int == 0:
            game.move_racket(player["id"], -1)
            key_int = 2

        if key_int == 1:
            game.move_racket(player["id"], 1)
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
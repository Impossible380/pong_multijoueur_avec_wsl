from pong_terminal import *
import time


class Game:
    def __init__(self, players):
        self.players = players
        self.screen = (120, 24)

        self.ball_default_position = (60, 14)
        self.racket_1_default_position = (20, 14)
        self.racket_2_default_position = (100, 14)

        self.ball = Entity("yellow", self.ball_default_position)
        self.racket_1 = Entity("blue", self.racket_1_default_position)
        self.racket_2 = Entity("red", self.racket_2_default_position)
    
    def goal(self, axis_move_ball):
        self.ball.position = list(self.ball_default_position)
        self.racket_1.position = list(self.racket_1_default_position)
        self.racket_2.position = list(self.racket_2_default_position)
        time.sleep(1)
        return -axis_move_ball
    
    def ball_touch_wall(self, axis, axis_move_ball):
        if axis == 0:
            if self.ball.position[0] + 2 >= self.screen[0]:
                self.players[0]["score"] += 1

                axis_move_ball = self.goal(axis_move_ball)
            
            elif self.ball.position[0] <= 0:
                self.players[1]["score"] += 1

                axis_move_ball = self.goal(axis_move_ball)
                
        else:
            if self.ball.position[1] <= 4 or \
                    self.ball.position[1] >= self.screen[1]:
                self.ball.position[1] -= axis_move_ball
                axis_move_ball = -axis_move_ball
        
        return axis_move_ball
    
    def ball_touch_racket(self, x_move_ball, y_move_ball, player_id):
        racket = self.racket_1 if player_id == 1 else self.racket_2

        if self.ball.position[0] + 4 >= racket.position[0] and \
                self.ball.position[0] - 2 <= racket.position[0] and \
                self.ball.position[1] >= racket.position[1] - 2 and \
                self.ball.position[1] <= racket.position[1] + 2:
            
            if self.ball.position[0] + 2 <= racket.position[0] or \
                    self.ball.position[0] >= racket.position[0]:
                self.ball.position[0] -= x_move_ball
                x_move_ball = -x_move_ball
            
            if self.ball.position[1] <= racket.position[1] - 2 or \
                    self.ball.position[1] >= racket.position[1] + 2:
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
    
        time.sleep(0.1)
        
        return x_move_ball, y_move_ball
    
    def move_racket(self, id, y_move_racket):
        racket = self.racket_1 if id == 1 else self.racket_2

        racket.position[1] += y_move_racket

        if racket.position[1] < 7 or racket.position[1] > self.screen[1] - 3:
            racket.position[1] -= y_move_racket


class Entity:
    def __init__(self, color, position):
        self.color = color
        self.position = list(position)
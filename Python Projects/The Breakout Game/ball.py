from turtle import Turtle
import random

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        start_x = random.randint(-300, 300)
        start_direction = random.choice([-1,1])
        self.goto(250,50)
        self.x_move = 10 * start_direction
        self.y_move = -10
        self.move_speed = 0.03

    def move(self):
        self.speed("fastest")
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x,new_y)

    def bounce_y(self):
        self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1










from turtle import Turtle
GAME_FONT = ("Courier", 24, "normal")
SCORE_FONT = ("Courier", 15, "normal")
ALIGNMENT = "center"

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.color("white")
        self.score = 0

    def game_over(self):
        self.goto(0, -20)
        self.write("Game Over!", font=GAME_FONT, align=ALIGNMENT)

    def score_board(self):
        self.penup()
        self.goto(-440, 275)
        self.write(f"Score: {self.score}", font=SCORE_FONT, align="left")

    def score_up(self):
        self.score += 10
        self.clear()
        self.score_board()

    def win(self):
        self.goto(0, -20)
        self.write("Hooray! You win!", font=GAME_FONT, align=ALIGNMENT)
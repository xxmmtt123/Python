import time
from turtle import Turtle, Screen
from paddle import Paddle
import selection
from ball import Ball
from block import Block
from scoreboard import Scoreboard

screen = Screen()
screen.setup(width=900, height=600)
screen.bgcolor("black")
screen.title("Breakout Game")

# Prevent window resizing
screen.cv._rootwindow.resizable(False, False)

# Disable automatic screen updates for performance
screen.tracer(0)

paddle = Paddle()
ball = Ball()
blocks = Block()
scoreboard = Scoreboard()

select_mode = False
select_level = False


def on_click(x, y):
    global select_mode, ball
    inside = selection.detect_method_selection(x, y, paddle, screen)
    if inside:
        select_mode = True
    else:
        select_mode = False


selection.display_method_selection(screen)

blocks.new_block()
blocks.hide_block()

ball.hideturtle()

game_is_on = True
while game_is_on:
    screen.update()
    screen.onclick(on_click)

    if select_mode:
        ball.showturtle()
        blocks.show_block()
        scoreboard.score_board()
        ball.move()
        time.sleep(ball.move_speed)

        if ball.xcor() > 420 or ball.xcor() < -420:
            ball.bounce_x()

        if (
                abs(ball.xcor() - paddle.paddle.xcor()) < (9 * 20) and
                abs(ball.ycor() - paddle.paddle.ycor()) < (1.3 * 20)
        ) or ball.ycor() > 290:
            ball.bounce_y()

        if ball.ycor() < -300:
            scoreboard.game_over()
            game_is_on = False

        for block in blocks.all_blocks:
            if (
                    abs(ball.xcor() - block.xcor()) < (4 * 10) and
                    abs(ball.ycor() - block.ycor()) < (1 * 20)
            ):
                ball.bounce_y()
                block.hideturtle()
                blocks.all_blocks.remove(block)
                scoreboard.score_up()

        if scoreboard.score == 600:
            screen.update()
            time.sleep(0.1)
            scoreboard.win()
            game_is_on = False




screen.exitonclick()


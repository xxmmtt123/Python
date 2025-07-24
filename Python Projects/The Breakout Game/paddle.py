from turtle import Turtle

LENGTH = 9
WIDTH = 1.3

class Paddle:
    def __init__(self):
        self.paddle = Turtle()
        self.paddle.shape("square")
        self.paddle.color("white")
        self.paddle.shapesize(stretch_len=LENGTH, stretch_wid=WIDTH)
        self.paddle.penup()
        self.paddle.setpos(0, -270)

    def move_left(self):
        new_x = self.paddle.xcor() - 50
        if new_x > -401:
            self.paddle.goto(new_x, -270)

    def move_right(self):
        new_x = self.paddle.xcor() + 50
        if new_x < 370:
            self.paddle.goto(new_x, -270)

    def move_to_x(self, x):
        new_x = x

        # Make sure the paddle is within the limit even though the mouse is outside the boundaries.
        if new_x < -370:
            new_x = -370
        elif new_x > 370:
            new_x = 370

        self.paddle.setx(new_x)

    def track_mouse(self, screen):
        # Determine the exact horizontal position where the paddle should go, based on the mouse’s current position.
        mouse_x = screen.cv.winfo_pointerx() - screen.cv.winfo_rootx() - 500
        # winfo_pointerx() gives the mouse position in screen coordinates
        # winfo_rootx() gives the position of the left edge of the window relative to the screen.
        # It tells us where the window is positioned on the screen.

        # Move the paddle based on mouse's x position
        self.move_to_x(mouse_x)

        # Continuously call this function to update the position
        screen.ontimer(lambda: self.track_mouse(screen), 20)  # Update the paddle every 20ms
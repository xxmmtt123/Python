from turtle import Turtle

method_selection_turtles = []
level_selection_turtles = []

def method_draw_box(x, y, width, height, border_color="white", fill_color="black"):
    box = Turtle()
    box.hideturtle()
    box.penup()
    box.color(border_color, fill_color)
    box.goto(x - width // 2, y - height // 2)
    box.pendown()
    box.begin_fill()
    for _ in range(2):
        box.forward(width)
        box.left(90)
        box.forward(height)
        box.left(90)
    box.end_fill()
    method_selection_turtles.append(box)


def display_method_selection(screen):
    title = Turtle()
    title.hideturtle()
    title.color("white")
    title.penup()
    title.goto(0, 100)
    title.write("Select Control Method: (Mouse / Keyboard)", align="center", font=("Arial", 16, "normal"))
    method_selection_turtles.append(title)

    method_draw_box(0, 50, 200, 40, border_color="green", fill_color="black")
    mouse_text = Turtle()
    mouse_text.hideturtle()
    mouse_text.color("green")
    mouse_text.penup()
    mouse_text.goto(0, 40)
    mouse_text.write("Mouse Control", align="center", font=("Arial", 14, "normal"))
    method_selection_turtles.append(mouse_text)

    method_draw_box(0, -30, 200, 40, border_color="blue", fill_color="black")
    keyboard_text = Turtle()
    keyboard_text.hideturtle()
    keyboard_text.color("blue")
    keyboard_text.penup()
    keyboard_text.goto(0, -40)
    keyboard_text.write("Keyboard Control", align="center", font=("Arial", 14, "normal"))
    method_selection_turtles.append(keyboard_text)

    screen.update()


def hide_method_selection():
    for turtle in method_selection_turtles:
        turtle.clear()
        turtle.hideturtle()

def use_mouse(paddle, screen):
    hide_method_selection()
    paddle.track_mouse(screen)


def use_keyboard(paddle, screen):
    hide_method_selection()
    screen.listen()
    screen.onkey(paddle.move_left, "Left")
    screen.onkey(paddle.move_right, "Right")


def detect_method_selection(x, y, paddle, screen):
    if -100 < x < 100 and 25 < y < 75:
        use_mouse(paddle, screen)
        return True
    elif -100 < x < 100 and -75 < y < -25:
        use_keyboard(paddle, screen)
        return True
    return False

from turtle import Turtle

LENGTH = 4
WIDTH = 1

num_blocks = 0

class Block:
    def __init__(self):
        self.all_blocks = []

    def new_block(self):
        global num_blocks
        blocks_per_row = 10
        total_blocks = 60

        for i in range(total_blocks):
            new_block = Turtle()
            new_block.shape("square")
            new_block.shapesize(stretch_len=LENGTH, stretch_wid=WIDTH)
            new_block.penup()

            row = i // blocks_per_row
            col = i % blocks_per_row

            if row in [0, 1]:
                new_block.color("#15AAE6")
            elif row in [2, 3]:
                new_block.color("#E6B015")
            else:
                new_block.color("#15E6AF")

            x_position = -410 + col * (LENGTH * 20 + 10)
            y_position = 70 + row * (WIDTH * 20 + 10)
            new_block.setpos(x_position, y_position)

            self.all_blocks.append(new_block)


    def hide_block(self):
        for block in self.all_blocks:
            block.hideturtle()

    def show_block(self):
        for block in self.all_blocks:
            block.showturtle()


from Position import Position
from Direction import Direction


# Snake class
class Snake:
    # Snake constructor
    def __init__(self):
        self.name = "snake"
        # TODO: better body generation
        self.body = [Position(0, 1), Position(0, 0), Position(1, 0), Position(2, 0), Position(3, 0)]
        self.direction = Direction.DOWN
        self.previous_direction = Direction.NULL

    # Makes the snake move one tick
    def move(self, apple):
        new_body = self.body
        new_body = [new_body[0].get_next_position(self.direction)] + new_body[:-1]
        self.previous_direction = self.direction
        self.body = new_body

        ate_apple = self.checkApple(apple)
        if ate_apple:
            # Duplicate the last body part
            self.body = new_body + new_body[-1:]

        return ate_apple

    # Returns true if the snake ran in a wall / body
    # False otherwise
    def checkCollision(self, b_width, b_height):
        if self.body[0].x == b_width or self.body[0].x < 0:
            return True
        elif self.body[0].y == b_height or self.body[0].y < 0:
            return True
        for i in range(1, len(self.body)):
            if self.body[0].x == self.body[i].x and self.body[0].y == self.body[i].y:
                return True
        return False

    # Returns true if the snake's head is on an apple
    # False otherwise
    def checkApple(self, apple):
        return self.body[0].x == apple.pos.x and self.body[0].y == apple.pos.y

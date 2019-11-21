from Direction import Direction


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_next_position(self, direction):
        x = self.x
        y = self.y
        if direction == Direction.LEFT:
            x -= 1
        if direction == Direction.RIGHT:
            x += 1
        if direction == Direction.UP:
            y -= 1
        if direction == Direction.DOWN:
            y += 1
        return Position(x, y)

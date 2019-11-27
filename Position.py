from Direction import Direction


# Position class, it's a set of positions (x,y)
class Position:
    # Position constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "X-" + str(self.x) + " | Y:" + str(self.y)

    # get the next position based on direction
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

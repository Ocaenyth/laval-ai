from Direction import Direction
from Position import Position


class Snake:
    def __init__(self):
        self.name = "snake"
        # TODO: better body generation
        self.body = [Position(0, 0), Position(1, 0), Position(2, 0), Position(3, 0)]
        self.direction = Direction.DOWN

    def move(self):
        new_body = self.body
        new_body = [new_body[0].get_next_position(self.direction)] + new_body[:-1]
        self.body = new_body
#         TODO: handle collision

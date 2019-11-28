import enum


# Simple enumeration class for the snake Direction
class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    NULL = 4

    # Static method to check if a new direction is valid
    @staticmethod
    def is_movement_valid(prev, new):
        if new == Direction.NULL:
            return False
        if prev == Direction.UP and new == Direction.DOWN:
            return False
        if prev == Direction.DOWN and new == Direction.UP:
            return False
        if prev == Direction.LEFT and new == Direction.RIGHT:
            return False
        if prev == Direction.RIGHT and new == Direction.LEFT:
            return False
        return True

    # Static method to get a direction from a set of
    # position and move
    @staticmethod
    def get_direction_from_pos_move(pos, move):
        if move.x - pos.x < 0:
            return Direction.LEFT
        elif move.x - pos.x > 0:
            return Direction.RIGHT
        elif move.y - pos.y > 0:
            return Direction.DOWN
        elif move.y - pos.y < 0:
            return Direction.UP

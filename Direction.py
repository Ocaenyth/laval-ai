import enum


class Direction(enum.Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    NULL = 4

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

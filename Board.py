import pygame

from Apple import Apple
from Direction import Direction
from Snake import Snake

TILE_SIZE = 20
TILE_COLOR = (255, 255, 255)
APPLE_COLOR = (212, 23, 23)
PLAYER_COLOR = (23, 212, 45)
PLAYER_HEAD_COLOR = (20, 163, 34)


class Board:
    def __init__(self, width, height):
        self.player = Snake()
        # TODO: get random position for apple
        self.apples = [Apple(0, 0), Apple(1, 1), Apple(2, 2), Apple(3, 3)]
        self.width = width
        self.height = height

    def compute_key(self, key):
        if key == pygame.K_ESCAPE:
            return False
        elif key == pygame.K_LEFT:
            self.player.direction = Direction.LEFT
            print("left")
        elif key == pygame.K_RIGHT:
            self.player.direction = Direction.RIGHT
            print("right")
        elif key == pygame.K_UP:
            self.player.direction = Direction.UP
            print("up")
        elif key == pygame.K_DOWN:
            self.player.direction = Direction.DOWN
            print("down")
        return True

    def update(self):
        self.player.move()

    def draw_board(self, window):
        window.fill(TILE_COLOR)
        self.draw_apples(window)
        self.draw_player(window)
        pygame.display.flip()

    def draw_apples(self, window):
        apple_width = TILE_SIZE / 2
        for apple in self.apples:
            pos = apple.pos

            x = pos.x * TILE_SIZE
            x += apple_width / 2

            y = pos.y * TILE_SIZE
            y += apple_width / 2

            pygame.draw.rect(window, APPLE_COLOR,
                             (x, y, apple_width, apple_width))

    def draw_player(self, window):
        offset = 2
        player_width = TILE_SIZE - offset * 2
        i = 0
        for pos in self.player.body:
            x = pos.x * TILE_SIZE
            x += offset

            y = pos.y * TILE_SIZE
            y += offset

            if i == 0:
                pygame.draw.rect(window, PLAYER_HEAD_COLOR, (x, y, player_width, player_width))
            else:
                pygame.draw.rect(window, PLAYER_COLOR, (x, y, player_width, player_width))
            i += 1

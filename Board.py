import time

import pygame

from Apple import Apple
from Direction import Direction
from Snake import Snake
from random import randrange

TILE_SIZE = 20
TILE_COLOR = (255, 255, 255)
APPLE_COLOR = (212, 23, 23)
PLAYER_COLOR = (23, 212, 45)
PLAYER_HEAD_COLOR = (20, 163, 34)


# Game board class
class Board:
    # Board constructor
    def __init__(self, width, height, aiPlayer=None):
        self.player = Snake()
        self.apple = Apple(randrange(width), randrange(height))
        self.width = width
        self.height = height
        self.aiPlayer = aiPlayer
        if aiPlayer is not None:
            self.moves = self.setMove()

    # Will do the appropriate action based on the key given
    def compute_key(self, key):
        tmp_direction = Direction.NULL
        if key == pygame.K_ESCAPE:
            return False
        elif key == pygame.K_LEFT:
            tmp_direction = Direction.LEFT
        elif key == pygame.K_RIGHT:
            tmp_direction = Direction.RIGHT
        elif key == pygame.K_UP:
            tmp_direction = Direction.UP
        elif key == pygame.K_DOWN:
            tmp_direction = Direction.DOWN

        # Make sure that the new direction is valid
        # (the snake cannot go back on UP if it was going DOWN)
        if Direction.is_movement_valid(self.player.previous_direction, tmp_direction):
            self.player.direction = tmp_direction

        return True

    # Update the game board and trigger potential events
    # (an apple was eaten or the snake ran in a wall / itself)
    def update(self):
        appleEaten = self.player.move(self.apple)
        if appleEaten:
            self.getNewApple()
        collision = self.player.checkCollision(self.width, self.height)
        if collision:
            return True

    # Redraw the board as to update it
    def draw_board(self, window):
        window.fill(TILE_COLOR)
        self.draw_apples(window)
        self.draw_player(window)
        pygame.display.flip()

    # Will draw the apples accordingly to their position
    def draw_apples(self, window):
        apple_width = TILE_SIZE / 2
        pos = self.apple.pos

        x = pos.x * TILE_SIZE
        x += apple_width / 2

        y = pos.y * TILE_SIZE
        y += apple_width / 2

        pygame.draw.rect(window, APPLE_COLOR,
                         (x, y, apple_width, apple_width))

    # Will draw the player body accordingly to its positions
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

    # Create a new apple
    def getNewApple(self):
        x = randrange(self.width)
        y = randrange(self.height)
        self.apple = Apple(x, y)
        # TODO: make sure the apple did not spawn on the player body
        if self.aiPlayer is not None:
            self.moves = self.setMove()

    # get player next move if it's an AI
    def getNextMove(self):
        nextMove = self.moves[0]
        self.moves.remove(nextMove)
        if nextMove.x - self.player.body[0].x < 0:
            return pygame.K_LEFT
        elif nextMove.x - self.player.body[0].x > 0:
            return pygame.K_RIGHT
        elif nextMove.y - self.player.body[0].y > 0:
            return pygame.K_DOWN
        elif nextMove.y - self.player.body[0].y < 0:
            return pygame.K_UP

    # Called when an apple is eaten
    # Get a new set of moves for the snake
    def setMove(self):
        return self.aiPlayer.getMove(self.player.body[0], self.apple.pos, self.player.direction)

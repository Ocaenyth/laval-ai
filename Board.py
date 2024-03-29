from random import randrange

import pygame

from Apple import Apple
from Direction import Direction
from Snake import Snake
from aStar import aStar

TILE_SIZE = 20
TILE_COLOR = (255, 255, 255)
APPLE_COLOR = (212, 23, 23)
PLAYER_COLOR = (23, 212, 45)
PLAYER_HEAD_COLOR = (20, 163, 34)
NEXT_MOVE_COLOR = (14, 188, 232)


# Game board class
class Board:
    # Board constructor
    def __init__(self, width, height, occurrences, ai, shortest, display_moves):
        self.occurrences = occurrences
        self.player = Snake()
        # Instanciate a dummy apple
        self.apple = Apple(0, 1)
        self.width = width
        self.height = height
        self.isAI = ai
        print(self.isAI)
        self.moves = None
        self.score = 0
        self.scores = []
        self.display_moves = display_moves
        self.shortest = shortest
        if ai:
            self.moves = self.setMove()
        self.getNewApple()

    def reset(self):
        self.player = Snake()
        self.getNewApple()
        self.score = 0
        if self.isAI:
            self.moves = self.setMove()
        pass

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
            self.score += 1
        collision = self.player.checkCollision(self.width, self.height)
        if collision:
            return True

    # Redraw the board as to update it
    def draw_board(self, window):
        window.fill(TILE_COLOR)
        self.draw_player(window)
        if self.isAI and self.display_moves:
            self.draw_next_moves(window)
        self.draw_apples(window)
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

    def draw_next_moves(self, window):
        offset = 2
        texture_width = TILE_SIZE - offset * 2
        color = NEXT_MOVE_COLOR
        tot_moves = len(self.moves) + 2

        pos = self.player.body[0]
        for move in self.moves:
            pos = pos.get_pos_from_move(move)
            # Actual drawing
            x = pos.x * TILE_SIZE
            x += offset

            y = pos.y * TILE_SIZE
            y += offset
            pygame.draw.rect(window, color, (x, y, texture_width, texture_width))

            r, g, b = color[0], color[1], color[2]
            r -= NEXT_MOVE_COLOR[0] / tot_moves
            g -= NEXT_MOVE_COLOR[1] / tot_moves
            b -= NEXT_MOVE_COLOR[2] / tot_moves
            color = (r, g, b)

    # Create a new apple
    def getNewApple(self):
        retry = True
        while retry:
            retry = False
            x = randrange(self.width)
            y = randrange(self.height)
            for b in self.player.body:
                if b.x == x and b.y == y:
                    retry = True
                    break
            if retry:
                continue
            self.apple = Apple(x, y)
            if self.isAI:
                self.moves = self.setMove()

    # post the AI's next move to pygame's event queue
    def post_next_move(self):
        rand_key = pygame.K_l
        nextMove = self.moves[0]

        # Set it to a useless key first
        event = pygame.event.Event(pygame.KEYDOWN, {"key": rand_key})
        if nextMove.x - self.player.body[0].x < 0:
            event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_LEFT})
        elif nextMove.x - self.player.body[0].x > 0:
            event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_RIGHT})
        elif nextMove.y - self.player.body[0].y > 0:
            event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DOWN})
        elif nextMove.y - self.player.body[0].y < 0:
            event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_UP})

        if event.key != rand_key:
            self.moves.remove(nextMove)
            pygame.event.post(event)

    # Called when an apple is eaten
    # Get a new set of moves for the snake
    def setMove(self):
        return aStar(self.player.body[0], self.apple.pos, self.player.direction, self.player.body,
                     self.height, self.width, self.shortest)

    def game_over(self, window, clock):
        width = self.width * TILE_SIZE
        height = self.height * TILE_SIZE
        s = pygame.Surface((width, height))  # the size of your rect
        s.set_alpha(128)  # alpha level
        s.fill((0, 0, 0))  # this fills the entire surface
        window.blit(s, (0, 0))

        fonts = pygame.font.get_fonts()
        font = pygame.font.SysFont(fonts[0], 15)
        # TODO : get total score
        t = "Average score: %.2f" % (self.get_total_score() / self.occurrences)
        text = font.render(t, True, (255, 255, 255), (0, 0, 0))
        rect = text.get_rect()
        rect.center = (width // 2, height // 2)
        window.blit(text, rect)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return False
            clock.tick(5)

    def get_total_score(self):
        total = 0
        print(self.scores)
        for score in self.scores:
            total += score
        print(total)
        return total

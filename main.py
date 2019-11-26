import pygame

from AiPlayer import AiPlayer
from Board import Board, TILE_SIZE

BOARD_WIDTH = 20
BOARD_HEIGHT = 20
FPS = 30
TPS = 10


def main(playerType):
    if playerType == "ai":
        board = Board(BOARD_WIDTH, BOARD_HEIGHT, AiPlayer())
        # board.setMove()
    else:
        board = Board(BOARD_WIDTH, BOARD_HEIGHT)
    tile_size = TILE_SIZE

    window_size = (board.width * tile_size, board.height * tile_size)
    window = pygame.display.set_mode(window_size)

    clock = pygame.time.Clock()
    run = True
    tick = 0

    while run:
        if playerType == "player":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    run = board.compute_key(event.key)
        elif playerType == "ai":
            move = board.getNextMove()
            run = board.compute_key(move)

        tick += 1
        if tick == FPS / TPS:
            gameOver = board.update()
            if (gameOver):
                board = Board(BOARD_WIDTH, BOARD_HEIGHT)
            tick = 0

        board.draw_board(window)
        clock.tick(FPS)


if __name__ == "__main__":
    main("player")

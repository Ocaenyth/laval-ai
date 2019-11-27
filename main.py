import pygame

from AiPlayer import AiPlayer
from Board import Board, TILE_SIZE

BOARD_WIDTH = 10
BOARD_HEIGHT = 10
FPS = 30
TPS = 100


def main(playerType):
    fps = FPS
    if playerType == "ai":
        board = Board(BOARD_WIDTH, BOARD_HEIGHT, AiPlayer())
        fps = TPS
    else:
        board = Board(BOARD_WIDTH, BOARD_HEIGHT)

    window_size = (board.width * TILE_SIZE, board.height * TILE_SIZE)
    window = pygame.display.set_mode(window_size)

    clock = pygame.time.Clock()
    run = True
    tick = 0

    pause = False
    while run:
        if pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pause = False
            clock.tick(fps)
            continue

        if playerType == "player":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pause = True
                elif event.type == pygame.KEYDOWN:
                    run = board.compute_key(event.key)
        elif playerType == "ai":
            move = board.getNextMove()
            run = board.compute_key(move)

        tick += 1
        if tick >= fps / TPS or playerType == "ai":
            gameOver = board.update()
            if (gameOver):
                if playerType == "ai":
                    board = Board(BOARD_WIDTH, BOARD_HEIGHT, AiPlayer())
                else:
                    board = Board(BOARD_WIDTH, BOARD_HEIGHT)
            tick = 0

        board.draw_board(window)
        clock.tick(fps)


if __name__ == "__main__":
    main("ai")

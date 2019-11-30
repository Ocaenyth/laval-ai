import pygame

from AiPlayer import AiPlayer
from Board import TILE_SIZE, Board

BOARD_WIDTH = 50
BOARD_HEIGHT = 50
FPS = 30
TPS = 1000
WINDOW_WIDTH = BOARD_WIDTH * TILE_SIZE
WINDOW_HEIGHT = BOARD_HEIGHT * TILE_SIZE


def main(playerType):
    pygame.init()
    occurences = 1
    current_occurence = 0

    fps = FPS
    if playerType == "ai":
        board = Board(BOARD_WIDTH, BOARD_HEIGHT, occurences, AiPlayer())
        fps = TPS
    else:
        board = Board(BOARD_WIDTH, BOARD_HEIGHT, occurences)

    window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
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
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    run = False
            clock.tick(fps)
            continue

        if playerType == "ai":
            board.post_next_move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = True
            elif event.type == pygame.KEYDOWN:
                run = board.compute_key(event.key)

        tick += 1
        if tick >= fps / TPS or playerType == "ai":
            gameOver = board.update()
            if gameOver or (playerType == "ai" and board.moves is None):
                current_occurence += 1
                cont = True
                board.scores.append(board.score)
                if current_occurence == occurences:
                    cont = board.game_over(window, clock)
                    current_occurence = 0
                    board = Board(BOARD_WIDTH, BOARD_HEIGHT, occurences, board.aiPlayer)
                if not cont:
                    return
                board.reset()
            tick = 0

        board.draw_board(window)
        clock.tick(fps)


if __name__ == "__main__":
    main("ai")

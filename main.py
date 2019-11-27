import pygame

from AiPlayer import AiPlayer
from Board import Board, TILE_SIZE

# Game board dimensions
BOARD_WIDTH = 20
BOARD_HEIGHT = 20
# Frames per second (framerate)
FPS = 30
# Gameplay ticks per second (game updates)
TPS = 10


def main(playerType):
    fps = FPS
    # Create board based on player type
    if playerType == "ai":
        board = Board(BOARD_WIDTH, BOARD_HEIGHT, AiPlayer())
        fps = TPS
        # board.setMove()
    else:
        board = Board(BOARD_WIDTH, BOARD_HEIGHT)

    # Create game window
    window_size = (board.width * TILE_SIZE, board.height * TILE_SIZE)
    window = pygame.display.set_mode(window_size)

    # Setup game variables
    clock = pygame.time.Clock()
    run = True
    tick = 0

    # Gameplay loop
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

        # Trigger a game update or not based on tick count
        # If TPS = 5 and FPS = 30, then there will be an update every 6 ticks (30 / 5 = 6)
        # or 6 updates per second
        tick += 1
        if tick >= fps / TPS or playerType == "ai":
            gameOver = board.update()
            if (gameOver):
                board = Board(BOARD_WIDTH, BOARD_HEIGHT)
            board.draw_board(window)
            tick = 0

        # Call that waits the appropriate amount of time in order
        # to have 30 (FPS = 30) frames per second
        clock.tick(fps)


if __name__ == "__main__":
    main("player")

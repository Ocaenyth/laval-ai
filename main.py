import pygame

from Board import TILE_SIZE, Board

import argparse


def parseArguments():
    parser = argparse.ArgumentParser(description="Let's play a game of Snake ! Or watch an AI do it !")
    parser.add_argument("-p", '--player', dest='player', action="store_true", help="If set, the AI will not play")
    parser.add_argument('-t', "--tps", metavar="", type=int, dest='tps', default=10,
                        help="Sets the rate at which the game will update (per second)")
    parser.add_argument('-f', "--fps", metavar="", type=int, dest='fps', default=30,
                        help="Sets the rate at which the window will update. Fps will always favor the highest "
                             "between TPS and FPS")
    parser.add_argument('-o', "--occurrences", metavar="", type=int, dest='occurrences', default=1,
                        help="Sets the amount of games to play before triggering game over.")
    parser.add_argument('-bw', "--board-width", metavar="", type=int, dest='width', default=20,
                        help="Sets the board's width")
    parser.add_argument('-bh', "--board-height", metavar="",
                        type=int, dest='height', default=20, help="Sets the board's height")
    parser.add_argument('-l', "--longest", dest='longest', action="store_true",
                        help="If set, the AI will use the reverse A* algorithm instead")
    parser.add_argument('-d', "--display-moves", dest='display', action="store_true",
                        help="If set, the AI's movements will be displayed on screen")

    args = parser.parse_args()
    print(args)

    return args


def main():
    pygame.init()

    current_occurrence = 0

    args = parseArguments()
    print(args)

    tps = args.tps
    fps = max(tps, args.fps)
    board = Board(args.width, args.height, args.occurrences, not args.player, not args.longest, args.display)
    if board.isAI:
        fps = args.tps

    window_size = (args.width * TILE_SIZE, args.height * TILE_SIZE)
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

        if board.isAI:
            board.post_next_move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = True
            elif event.type == pygame.KEYDOWN:
                run = board.compute_key(event.key)

        tick += 1
        if tick >= fps / tps or board.isAI:
            gameOver = board.update()
            if gameOver or (board.isAI and board.moves is None):
                current_occurrence += 1
                cont = True
                board.scores.append(board.score)
                if current_occurrence == args.occurrences:
                    cont = board.game_over(window, clock)
                    if not cont:
                        return
                    current_occurrence = 0
                    board = Board(board.width, board.height, board.occurrences, board.isAI, board.shortest,
                                  board.display_moves)
                board.reset()
            tick = 0

        board.draw_board(window)
        clock.tick(fps)


if __name__ == "__main__":
    main()

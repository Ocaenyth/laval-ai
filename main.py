import pygame

from Board import TILE_SIZE, Board

import argparse


FPS = 30



def parseArguments():
    parser = argparse.ArgumentParser(description='argument')
    parser.add_argument('-p', metavar='player', type=bool, dest='player', default=False)
    parser.add_argument('-t', metavar='tick', type=int, dest='tick', default=5)
    parser.add_argument('-o', metavar='occurence', type=int, dest='occurence', default=1)
    parser.add_argument('-bw', metavar='width', type=int, dest='width', default=20)
    parser.add_argument('-bh', metavar='height', type=int, dest='height', default=20)
    parser.add_argument('-s', metavar='ia', type=bool, dest='ia', default=True)
    parser.add_argument('-d', metavar='affichage', type=bool, dest='affichage', default=True)

    args = parser.parse_args()

    print(args)

    return args


def main():
    pygame.init()
    
    current_occurence = 0

    args = parseArguments()

    fps = FPS
    board = Board(args.width, args.height, args.occurence, aiPlayer=not args.player, shortest=args.ia)
    if not args.player:
        fps = args.tick

    window_size = (args.width * TILE_SIZE,  args.height * TILE_SIZE)
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

        if not args.player:
            board.post_next_move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = True
            elif event.type == pygame.KEYDOWN:
                run = board.compute_key(event.key)

        tick += 1
        if tick >= fps / args.tick or not args.player:
            gameOver = board.update()
            if gameOver or (not args.player and board.moves is None):
                current_occurence += 1
                cont = True
                board.scores.append(board.score)
                if current_occurence == args.occurence:
                    cont = board.game_over(window, clock)
                    current_occurence = 0
                    board = Board(args.width, args.height, args.occurence, aiPlayer=not args.player, shortest=args.ia)
                if not cont:
                    return
                board.reset()
            tick = 0

        board.draw_board(window)
        clock.tick(fps)


if __name__ == "__main__":
    main()

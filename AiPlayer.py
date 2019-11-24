from aStar import aStar


class AiPlayer:

    def play(self):
        nextMove = self.move[0]
        self.move.pop(nextMove)

    def getMove(self, start, end):
        return aStar(start, end)

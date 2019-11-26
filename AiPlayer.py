from aStar import aStar


class AiPlayer:

    def getMove(self, start, end, direction):
        return aStar(start, end, direction)

from aStar import aStar


class AiPlayer:

    def getMove(self, start, end, direction, body, height, width):
        return aStar(start, end, direction, body, height, width)

from Position import Position


class Node:
    def __init__(self, position, parent):
        self.position = position
        self.f = 0
        self.h = 0
        self.g = 0
        self.parents = parent

    def __eq__(self, other):
        return self.position.x == other.position.x and self.position.y == other.position.y


def aStar(position, goal):
    openList = []
    closeList = []

    start = Node(position, None)
    end = Node(goal, None)
    openList.append(start)

    while len(openList) > 0:
        node = min(openList, key=lambda x: x.f)
        openList.remove(node)
        closeList.append(node)

        if node == end:
            solution = []
            while node is not None:
                solution.append(node.position)
                node = node.parents
            return solution

        children = [Node(Position(node.position.x + 1, node.position.y), node),
                    Node(Position(node.position.x - 1, node.position.y), node),
                    Node(Position(node.position.x, node.position.y + 1), node),
                    Node(Position(node.position.x, node.position.y - 1), node)]

        inClose = False
        inOpen = False
        for child in children:
            for closed in closeList:
                if child == closed:
                    inClose = True
                    break
            if inClose:
                pass
            if child.position.x >= 0 and child.position.y >= 0:
                child.g = node.g + 1
                child.h = abs(child.position.x - end.position.x) + abs(child.position.y - end.position.y)
                child.f = child.g + child.h
                for openNode in openList:
                    if child == openNode and child.g >= openNode.g:
                        inOpen = True
                        break
                if inOpen:
                    continue
                openList.append(child)
            else:
                pass

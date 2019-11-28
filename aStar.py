from Direction import Direction


class Node:
    def __init__(self, position, parent, direction):
        self.position = position
        self.direction = direction
        self.f = 0
        self.h = 0
        self.g = 0
        self.parents = parent

    def __eq__(self, other):
        return self.position.x == other.position.x and self.position.y == other.position.y


def aStar(position, goal, direction, body, height, width):
    openList = []
    closeList = []

    start = Node(position, None, direction)
    end = Node(goal, None, None)
    openList.append(start)

    while len(openList) > 0:
        node = min(openList, key=lambda x: x.f)
        openList.remove(node)
        closeList.append(node)

        if node == end:
            return getSolution(node)

        children = getChildren(node)

        for child in children:
            if isInClose(child, closeList):
                continue
            if 0 <= child.position.x <= width and 0 <= child.position.y <= height:
                updateChild(child, end, node)
                if isInOpen(child, openList):
                    continue
                if isInBody(child, body):
                    continue
                openList.append(child)


def getChildren(node):
    children = []
    if node.direction == Direction.UP:
        children = [Node(node.position.get_next_position(Direction.RIGHT), node, Direction.RIGHT),
                    Node(node.position.get_next_position(Direction.LEFT), node, Direction.LEFT),
                    Node(node.position.get_next_position(Direction.UP), node, Direction.UP)]
    elif node.direction == Direction.LEFT:
        children = [Node(node.position.get_next_position(Direction.LEFT), node, Direction.LEFT),
                    Node(node.position.get_next_position(Direction.UP), node, Direction.UP),
                    Node(node.position.get_next_position(Direction.DOWN), node, Direction.DOWN)]
    elif node.direction == Direction.RIGHT:
        children = [Node(node.position.get_next_position(Direction.RIGHT), node, Direction.RIGHT),
                    Node(node.position.get_next_position(Direction.UP), node, Direction.UP),
                    Node(node.position.get_next_position(Direction.DOWN), node, Direction.DOWN)]
    elif node.direction == Direction.DOWN:
        children = [Node(node.position.get_next_position(Direction.RIGHT), node, Direction.RIGHT),
                    Node(node.position.get_next_position(Direction.LEFT), node, Direction.LEFT),
                    Node(node.position.get_next_position(Direction.DOWN), node, Direction.DOWN)]
    return children


def isInClose(child, closeList):
    for closed in closeList:
        if child == closed:
            return True
    return False


def isInOpen(child, openList):
    for openNode in openList:
        if child == openNode and child.g >= openNode.g:
            return True
    return False


def isInBody(child, body):
    for position in body:
        if child.position.x == position.x and child.position.y == position.y:
            return True
    return False


def updateChild(child, end, node):
    child.g = node.g + 1
    child.h = abs(child.position.x - end.position.x) + abs(child.position.y - end.position.y)
    child.f = child.g + child.h


def getSolution(node):
    solution = []
    while node is not None:
        solution.append(node.position)
        node = node.parents
    solution = list(reversed(solution))
    solution.pop(0)
    return solution

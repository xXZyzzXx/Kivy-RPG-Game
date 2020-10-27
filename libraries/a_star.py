from collections import deque


def screenToLinear(scrx, scry):
    linx = scrx - scry // 2
    liny = -scrx - (scry + 1) // 2
    return linx, liny


def linearToScreen(linx, liny):
    rotx = (linx - liny) // 2
    roty = (-linx - liny)
    return rotx, roty


class PathNode:
    def __init__(self):
        self.value = 0
        self.prev = None

    def __str__(self):
        return '{:3}'.format(self.value)


fwidth = 25
fheight = 50
costField = [[0 for _ in range(fheight)] for _ in range(fwidth)]
pathField = [[PathNode() for _ in range(fheight)] for _ in range(fwidth)]


def inField(x, y):
    return 0 <= x < fwidth and 0 <= y < fheight


def clearPathField():
    for x in range(fwidth):
        for y in range(fheight):
            pathField[x][y].value = 0
            pathField[x][y].prev = None


sideStepCost = 10
cornerStepCost = 15


def sidesOf(x, y):
    if y % 2 == 0:
        return [(x - 1, y - 1), (x - 1, y + 1), (x, y - 1), (x, y + 1)]
    else:
        return [(x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y + 1)]


def cornersOf(x, y):
    return [(x - 1, y), (x + 1, y), (x, y - 2), (x, y + 2)]


def updatePathFieldNode(cx, cy, pending):
    baseValue = pathField[cx][cy].value
    for x, y in sidesOf(cx, cy):
        if inField(x, y):
            newValue = baseValue - sideStepCost - costField[x][y]
            if newValue > pathField[x][y].value:
                pathField[x][y].value = newValue
                pathField[x][y].prev = (cx, cy)
                pending.append((x, y))
    for x, y in cornersOf(cx, cy):
        if inField(x, y):
            newValue = baseValue - cornerStepCost - costField[x][y]
            if newValue > pathField[x][y].value:
                pathField[x][y].value = newValue
                pathField[x][y].prev = (cx, cy)
                pending.append((x, y))


def generatePathField(initx, inity, initValue):
    clearPathField()
    pending = deque()
    if inField(initx, inity):
        pathField[initx][inity].value = initValue
        pending.append((initx, inity))
    while len(pending) != 0:
        (x, y) = pending.popleft()
        updatePathFieldNode(x, y, pending)


def buildPathTo(x, y):
    path = []
    current = (x, y)
    while current is not None:
        path.insert(0, current)
        cx, cy = current
        current = pathField[cx][cy].prev
    return path


def create_move_map(posX, posY, points):
    generatePathField(posX, posY, points)
    moves_list = []
    for x in range(fwidth):
        for y in range(fheight):
            if pathField[x][y].value != 0:
                moves_list.append(buildPathTo(x, y))
    return moves_list




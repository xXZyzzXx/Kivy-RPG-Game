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


fwidth = 15
fheight = 30
costField = [[0 for _ in range(fheight)] for _ in range(fwidth)]
pathField = [[PathNode() for _ in range(fheight)] for _ in range(fwidth)]


def inField(x, y):
    return 0 <= x < fwidth and 0 <= y < fheight


def printPathField():
    for y in range(fheight):
        if y % 2 == 1:
            print(end='  ')
        for x in range(fwidth):
            if 0 < costField[x][y] <= 50:
                print('\033[93m', end='')
            elif 50 < costField[x][y]:
                print('\033[91m', end='')
            print(pathField[x][y], end='')
            if 0 < costField[x][y]:
                print('\033[0m', end='')
            print(end=' ')
        print()


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


for x in range(6, 9):
    for y in range(9, 12):
        costField[x][y] = 20
costField[7][13] = float('inf')
generatePathField(7, 12, 100)
printPathField()

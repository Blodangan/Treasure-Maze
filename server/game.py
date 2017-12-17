from math import cos, sin
from random import randint
from time import time
from server.player import Player
from utils.funcs import raycast
from utils.consts import Constants

class Game():
    def __init__(self):
        self.players = [None] * 4
        self.mazeSize = Constants.MAZE_SIZE
        self.startingPos = [(1.5, 1.5),
                            (self.mazeSize - 1.5, 1.5),
                            (self.mazeSize - 1.5, self.mazeSize - 1.5),
                            (1.5, self.mazeSize - 1.5)]
        self.startingRot = [45, 135, -45, -135]
        self.treasurePos = (self.mazeSize / 2.0, self.mazeSize / 2.0)
        self.maze = self.buildMaze()
        self.winner = ""

    def register(self, name):
        players = self.players

        id = -1
        for i in range(len(players)):
            if players[i] == None:
                id = i
                break

        if id == -1:
            return (Constants.RESPONSE_FAILURE, "Too many players registered")

        pos = self.startingPos[id]
        rot = self.startingRot[id]
        player = Player(name, pos, rot)

        players[id] = player

        return (Constants.RESPONSE_SUCCESS, id)

    def unregister(self, id):
        player = self.players[id]

        if player.hasTreasure:
            self.treasurePos = player.pos

        self.players[id] = None

        return (Constants.RESPONSE_SUCCESS, 0)

    def getTreasure(self, player):
        if self.treasurePos == None:
            return

        dx = player.pos[0] - self.treasurePos[0]
        dy = player.pos[1] - self.treasurePos[1]
        distSq = dx * dx + dy * dy
        r = player.radius

        if distSq <= r * r:
            player.hasTreasure = True
            player.dirSpeed = Constants.SPEED_TREASURE
            self.treasurePos = None

    def win(self, player):
        if not player.hasTreasure:
            return

        dx = player.pos[0] - player.spawn[0]
        dy = player.pos[1] - player.spawn[1]
        distSq = dx * dx + dy * dy
        r = player.radius

        if distSq <= r * r:
            self.winner = player.name

    def collision(self, pos, radius):
        x, y = pos
        x1 = int(x - radius)
        y1 = int(y - radius)
        x2 = int(x + radius)
        y2 = int(y + radius)

        for i in (y1, y2):
            for j in (x1, x2):
                if self.maze[i][j] != 0:
                    return True

        return False

    def movePlayer(self, player, dir):
        x, y = player.pos
        dx, dy = dir
        speed = player.dirSpeed

        player.pos = (x + speed * dx, y + speed * dy)
        if not self.collision(player.pos, player.radius):
            return

        if dx != 0:
            player.pos = (x + speed * dx, y)
            if not self.collision(player.pos, player.radius):
                return

        if dy != 0:
            player.pos = (x, y + speed * dy)
            if not self.collision(player.pos, player.radius):
                return

        player.pos = (x, y)

    def move(self, id, dir):
        player = self.players[id]

        if dir not in ("up", "down"):
            return (Constants.RESPONSE_SUCCESS, player.pos)

        dx, dy = player.dir
        if dir == "down":
            dx, dy = -dx, -dy

        self.movePlayer(player, (dx, dy))
        self.getTreasure(player)
        self.win(player)

        return (Constants.RESPONSE_SUCCESS, player.pos)

    def rotate(self, id, dir):
        player = self.players[id]

        if dir == "left":
            player.rot += player.rotSpeed
        elif dir == "right":
            player.rot -= player.rotSpeed

        player.dir = (cos(player.rot), sin(player.rot))

        return (Constants.RESPONSE_SUCCESS, (player.rot, player.dir))

    def kill(self, id):
        player = self.players[id]

        if player.hasTreasure:
            self.treasurePos = player.pos
            player.hasTreasure = False
            player.dirSpeed = Constants.SPEED
            player.pos = player.spawn

    def shoot(self, id):
        player = self.players[id]

        t = time()

        if (t - player.lastShot) < Constants.SHOT_DELAY:
            return (Constants.RESPONSE_SUCCESS, False)

        posX, posY = player.pos
        dirX, dirY = player.dir

        targets = []

        for i in range(len(self.players)):
            if i == id:
                continue

            other = self.players[i]
            if other == None:
                continue

            otherX, otherY = other.pos
            radius = other.radius

            (dx, dy) = (otherX - posX, otherY - posY)
            d = dx * dirX + dy * dirY

            linePointX, linePointY = (dx - d * dirX, dy - d * dirY)
            linePointDistSq = linePointX * linePointX + linePointY * linePointY
            if linePointDistSq <= radius * radius:
                if 0 < d and d < raycast(self.maze, player.pos, player.dir)[0]:
                    targets.append((d, i))

        if len(targets) >= 1:
            targets.sort()
            self.kill(targets[0][1])

        player.lastShot = t

        return (Constants.RESPONSE_SUCCESS, True)

    def getUpdates(self, id):
        player = self.players[id]

        playersUpdates = [(player.pos, player.hasTreasure)]

        for i in range(len(self.players)):
            if i == id:
                continue

            other = self.players[i]
            if other == None:
                continue

            pos = other.pos
            hasTreasure = other.hasTreasure

            playersUpdates.append((pos, hasTreasure))

        updates = (playersUpdates, self.treasurePos, self.winner)

        return (Constants.RESPONSE_SUCCESS, updates)

    def buildMaze(self):
        size = self.mazeSize

        maze = [[1 for j in range(size)] for i in range(size)]

        i, j = 1, 1
        maze[i][j] = 0
        hist = [(i, j)]

        while len(hist) != 0:
            dir = []
            if i - 2 > 0 and maze[i - 2][j] != 0:
                dir.append((-1, 0))
            if i + 2 < size - 1 and maze[i + 2][j] != 0:
                dir.append((1, 0))
            if j - 2 > 0 and maze[i][j - 2] != 0:
                dir.append((0, -1))
            if j + 2 < size - 1 and maze[i][j + 2] != 0:
                dir.append((0, 1))

            if len(dir) != 0:
                di, dj = dir[randint(0, len(dir) - 1)]
                maze[i + di][j + dj] = 0
                maze[i + 2 * di][j + 2 * dj] = 0
                i, j = i + 2 * di, j + 2 * dj
                hist.append((i, j))
            else:
                i, j = hist.pop()

        for i in range(1, size - 1):
            for j in range(1, size - 1):
                if maze[i][j] != 0 and randint(1, 100) <= 20:
                    maze[i][j] = 0

        x, y = int(self.treasurePos[0]), int(self.treasurePos[1])
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                maze[i][j] = 0

        return maze

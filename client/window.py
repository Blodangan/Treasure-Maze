from math import cos, tan, atan2, sqrt, pi, radians
import pygame
from utils.funcs import raycast
from utils.consts import Constants

class Window():
    def __init__(self, playerName):
        self.res = Constants.RESOLUTION
        self.colW = Constants.COLUMN_WIDTH
        self.screen = pygame.display.set_mode(self.res, pygame.DOUBLEBUF)
        self.fov = radians(Constants.FOV)
        self.screenDist = self.res[0] / (2.0 * tan(self.fov / 2.0))
        self.zbuffer = [0] * self.res[0]

        self.sprites = {}
        self.sprites[Constants.SPRITE_PLAYER] = pygame.image.load(Constants.SPRITE_PLAYER).convert_alpha()
        self.sprites[Constants.SPRITE_PLAYERTREASURE] = pygame.image.load(Constants.SPRITE_PLAYERTREASURE).convert_alpha()
        self.sprites[Constants.SPRITE_TREASURE] = pygame.image.load(Constants.SPRITE_TREASURE).convert_alpha()
        self.sprites[Constants.SPRITE_SPAWN] = pygame.image.load(Constants.SPRITE_SPAWN).convert_alpha()

        self.cursor = pygame.image.load(Constants.CURSOR).convert_alpha()

        pygame.display.set_caption(Constants.TITLE.format(playerName))

    def drawMaze(self, maze, player):
        w, h = self.res

        posX, posY = player.pos
        dirX, dirY = player.dir

        pygame.draw.rect(self.screen, (64, 64, 64), (0, 0, w, h / 2))
        pygame.draw.rect(self.screen, (128, 128, 128), (0, h / 2, w, h / 2))

        for x in range(0, w, self.colW):
            cameraX = x - w / 2.0

            rayDirX, rayDirY = self.screenDist * dirX + cameraX * dirY, self.screenDist * dirY - cameraX * dirX
            rayLength = sqrt(rayDirX * rayDirX + rayDirY * rayDirY)
            rayDirX, rayDirY = rayDirX / rayLength, rayDirY / rayLength

            dist, side = raycast(maze, (posX, posY), (rayDirX, rayDirY))
            dist *= (dirX * rayDirX + dirY * rayDirY)

            for i in range(self.colW):
                self.zbuffer[x + i] = dist

            height = self.screenDist / dist

            colorCoeff = int(128.0 / (1 + dist))
            color = (colorCoeff, 0, 0) if side == "x" else (0, 0, colorCoeff)

            yStart = max(int((h - height) / 2.0), 0)
            rect = (x, yStart, self.colW, min(int(height), h))

            pygame.draw.rect(self.screen, color, rect)

    def drawSprite(self, distSq, angle, spriteName):
        w, h = self.res

        dist = sqrt(distSq) * cos(angle)

        size = min(int(self.screenDist / dist), 3 * h)

        sprite = self.sprites[spriteName]
        spriteScaled = pygame.transform.scale(sprite, (size, size))

        cameraX = self.screenDist * tan(angle)

        xStart = int((w - size) / 2.0 - cameraX)
        yStart = int((h - size) / 2.0)

        for i in range(0, size, self.colW):
            x = xStart + i

            if x + self.colW <= 0:
                continue
            elif x  >= w:
                break

            if dist < self.zbuffer[x]:
                self.screen.blit(spriteScaled, (x, yStart), (i, 0, self.colW, size))

    def drawSprites(self, player, sprites):
        visibleSprites = []

        for spriteName, pos in sprites:
            dx = pos[0] - player.pos[0]
            dy = pos[1] - player.pos[1]

            angle = (atan2(dy, dx) - player.rot) % (2 * pi)
            if angle > pi:
                angle -= 2 * pi

            if abs(angle) >= pi / 2.0:
                continue

            distSq = dx * dx + dy * dy
            if distSq == 0:
                continue

            visibleSprites.append((distSq, angle, spriteName))

        visibleSprites.sort()

        for i in range(len(visibleSprites)):
            sprite = visibleSprites[len(visibleSprites) - i - 1]
            self.drawSprite(sprite[0], sprite[1], sprite[2])

    def draw(self, maze, player, otherPlayers, treasurePos, winner):
        self.drawMaze(maze, player)

        sprites = []

        for pos, hasTreasure in otherPlayers:
            spriteName = Constants.SPRITE_PLAYER if not hasTreasure else Constants.SPRITE_PLAYERTREASURE
            sprites.append((spriteName, pos))

        if treasurePos != None:
            sprites.append((Constants.SPRITE_TREASURE, treasurePos))

        sprites.append((Constants.SPRITE_SPAWN, player.spawn))

        self.drawSprites(player, sprites)

        if winner != "":
            font = pygame.font.SysFont("Times New Roman", 42, True)
            centered = font.render(Constants.WINNER_TEXT.format(winner), True, (255, 255, 255))
        else:
            centered = self.cursor

        xCentered = self.res[0] / 2 - centered.get_width() / 2
        yCentered = self.res[1] / 2 - centered.get_height() / 2
        self.screen.blit(centered, (xCentered, yCentered))

        if player.hasTreasure:
            font = pygame.font.SysFont("Times New Roman", 42, True)
            msg = font.render(Constants.TREASURE_TEXT, True, (216, 216, 216))
            xMsg = self.res[0] / 2 - msg.get_width() / 2
            yMsg = 0
            self.screen.blit(msg, (xMsg, yMsg))

        pygame.display.flip()

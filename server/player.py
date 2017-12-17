from math import cos, sin, radians
from utils.consts import Constants

class Player:
    def __init__(self, name, pos, rot):
        self.name = name
        self.pos = pos
        self.rot = radians(rot)
        self.rotSpeed = Constants.ROTATION_SPEED
        self.dir = (cos(self.rot), sin(self.rot))
        self.dirSpeed = Constants.SPEED
        self.radius = Constants.RADIUS
        self.hasTreasure = False
        self.spawn = self.pos
        self.lastShot = 0

import pygame
from client.requests import Requests
from client.window import Window
from client.player import Player
from utils.consts import Constants

class Client():
    def __init__(self, name, addr, port):
        pygame.init()

        self.requests = Requests(addr, port)
        self.window = Window(name)
        self.keyboard = {}
        self.maze = [[]]
        self.player = Player(name)
        self.otherPlayers = []
        self.treasurePos = None
        self.winner = ""
        self.soundShot = pygame.mixer.Sound(Constants.SOUND_SHOT)
        self.running = True

    def buildPlayer(self):
        requests = self.requests
        player = self.player

        response, player.id = requests.register(player.name)
        if response == Constants.RESPONSE_FAILURE:
            print(player.id)
            return False

        _, player.pos = requests.move(player.id, "None")
        _, (player.rot, player.dir) = requests.rotate(player.id, "None")
        player.spawn = player.pos

        return True

    def updateKeyboard(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.keyboard[event.key] = True
            elif event.type == pygame.KEYUP:
                self.keyboard[event.key] = False

    def keyPressed(self, key):
        keyboard = self.keyboard

        return key in keyboard.keys() and keyboard[key]

    def sendRequests(self):
        if self.winner != "":
            return

        requests = self.requests
        player = self.player

        if self.keyPressed(pygame.K_UP):
            requests.move(player.id, "up")
        if self.keyPressed(pygame.K_DOWN):
            requests.move(player.id, "down")
        if self.keyPressed(pygame.K_LEFT):
            _, (player.rot, player.dir) = requests.rotate(player.id, "left")
        if self.keyPressed(pygame.K_RIGHT):
            _, (player.rot, player.dir) = requests.rotate(player.id, "right")
        if self.keyPressed(pygame.K_SPACE):
            _, shot = requests.shoot(player.id)
            if shot:
                pygame.mixer.Sound.play(self.soundShot)

        _, (playersUpdates, self.treasurePos, self.winner) = requests.getUpdates(player.id)

        player.pos, player.hasTreasure = playersUpdates[0]
        self.otherPlayers = playersUpdates[1:]

    def run(self):
        _, self.maze = self.requests.getMaze()
        if not self.buildPlayer():
            return

        clock = pygame.time.Clock()

        while self.running:
            self.updateKeyboard()
            self.sendRequests()
            self.window.draw(self.maze, self.player, self.otherPlayers, self.treasurePos, self.winner)
            clock.tick(Constants.FPS)

        self.requests.unregister(self.player.id)

        pygame.quit()

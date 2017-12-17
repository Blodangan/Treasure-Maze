from http.server import HTTPServer
from server.requests import RequestHandler
from server.game import Game

class Server(HTTPServer):
    def __init__(self, addr, port):
        HTTPServer.__init__(self, (addr, port), RequestHandler)

        self.game = Game()
        self.running = True

    def run(self):
        while self.running:
            self.handle_request()

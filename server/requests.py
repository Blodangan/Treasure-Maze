from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from utils.consts import Constants

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        url = urlparse(self.path)

        func = url.path.rpartition("/")[2]
        params = parse_qs(url.query)

        response = self.getResponse(func, params)

        self.wfile.write(bytes(str(response), "utf-8"))

    def getResponse(self, func, params):
        game = self.server.game

        # REQUEST_STOP
        if func == Constants.REQUEST_STOP:
            self.server.running = False
            return (Constants.RESPONSE_SUCCESS, 0)

        # REQUEST_REGISTER
        if func == Constants.REQUEST_REGISTER:
            name = params[Constants.PARAM_NAME][0]
            return game.register(name)

        # REQUEST_UNREGISTER
        if func == Constants.REQUEST_UNREGISTER:
            id = int(params[Constants.PARAM_ID][0])
            return game.unregister(id)

        # REQUEST_GETMAZE
        if func == Constants.REQUEST_GETMAZE:
            return (Constants.RESPONSE_SUCCESS, game.maze)

        # REQUEST_MOVE
        if func == Constants.REQUEST_MOVE:
            id = int(params[Constants.PARAM_ID][0])
            dir = params[Constants.PARAM_DIR][0]
            return game.move(id, dir)

        # REQUEST_ROTATE
        if func == Constants.REQUEST_ROTATE:
            id = int(params[Constants.PARAM_ID][0])
            dir = params[Constants.PARAM_DIR][0]
            return game.rotate(id, dir)

        # REQUEST_SHOOT
        if func == Constants.REQUEST_SHOOT:
            id = int(params[Constants.PARAM_ID][0])
            return game.shoot(id)

        # REQUEST_GETUPDATES
        if func == Constants.REQUEST_GETUPDATES:
            id = int(params[Constants.PARAM_ID][0])
            return game.getUpdates(id)

        return (Constants.RESPONSE_FAILURE, "Bad Request")

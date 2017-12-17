import urllib.request
import ast
from utils.consts import Constants

class Requests():
    def __init__(self, addr, port):
        self.baseAddr = "http://" + addr + ":" + str(port) + "/"

    def query(self, func, params):
        q = ""

        for i in range(len(params)):
            p, arg = params[i]
            q += p + "=" + arg
            if i < len(params) - 1:
                q += "&"

        url = self.baseAddr + func + "?" + q
        res = urllib.request.urlopen(url).read().decode("utf-8")

        return ast.literal_eval(res)

    def stop(self):
        func = Constants.REQUEST_STOP
        params = []

        return self.query(func, params)

    def register(self, name):
        func = Constants.REQUEST_REGISTER
        params = [(Constants.PARAM_NAME, name)]

        return self.query(func, params)

    def unregister(self, id):
        func = Constants.REQUEST_UNREGISTER
        params = [(Constants.PARAM_ID, str(id))]

        return self.query(func, params)

    def getMaze(self):
        func = Constants.REQUEST_GETMAZE
        params = []

        return self.query(func, params)

    def move(self, id, dir):
        func = Constants.REQUEST_MOVE
        params = [(Constants.PARAM_ID, str(id)), (Constants.PARAM_DIR, dir)]

        return self.query(func, params)

    def rotate(self, id, dir):
        func = Constants.REQUEST_ROTATE
        params = [(Constants.PARAM_ID, str(id)), (Constants.PARAM_DIR, dir)]

        return self.query(func, params)

    def shoot(self, id):
        func = Constants.REQUEST_SHOOT
        params = [(Constants.PARAM_ID, str(id))]

        return self.query(func, params)

    def getUpdates(self, id):
        func = Constants.REQUEST_GETUPDATES
        params = [(Constants.PARAM_ID, str(id))]

        return self.query(func, params)

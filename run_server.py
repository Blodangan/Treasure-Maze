#!/usr/bin/env python3

from server.server import Server
from utils.consts import Constants

addr, port = "", Constants.SERVER_PORT
server = Server(addr, port)
server.run()

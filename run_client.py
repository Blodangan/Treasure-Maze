#!/usr/bin/env python3

import sys
from client.client import Client
from utils.consts import Constants

name = sys.argv[1] if len(sys.argv) >= 2 else "Noname"

addr, port = Constants.SERVER_ADDR, Constants.SERVER_PORT
client = Client(name, addr, port)
client.run()

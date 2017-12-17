# Treasure Maze

A multiplayer first-person shooter game.

The game is played by 2, 3 or 4 players. The goal is to find the treasure inside the maze and bring it back to your starting point. Be careful, other players can shoot you if you have the treasure.

A basic raycaster is used for rendering. While an UDP server is the best choice, an HTTP server is used.

![screenshot](https://raw.githubusercontent.com/Blodangan/Treasure-Maze/master/screenshot.png)

## Installation

Treasure Maze needs pygame. You can use pip to install it:
```bash
$ python3 -m pip install pygame
```

## Usage

Configuration (server address & port, resolution, ...) can be found in ``utils/consts.py``

Run the server:
```bash
$ ./run_server.py
```

Run the client:
```bash
$ ./run_client.py [username]
```

## License

Except for files in the ``assets`` folder, this code is released under the [MIT License](LICENSE).

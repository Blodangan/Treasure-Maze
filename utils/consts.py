class Constants:
    SERVER_ADDR = "127.0.0.1"
    SERVER_PORT = 8080

    RESOLUTION = (960, 540)
    COLUMN_WIDTH = 4
    FOV = 70
    FPS = 30

    MAZE_SIZE = 13
    ROTATION_SPEED = 0.1
    SPEED = 0.2
    SPEED_TREASURE = 0.1
    RADIUS = 0.4
    SHOT_DELAY = 2.0

    TITLE = "{} - Treasure Maze"
    WINNER_TEXT = "{} is the winner of the game!"
    TREASURE_TEXT = "You got the treasure! Run!"

    SPRITE_PLAYER = "assets/player.png"
    SPRITE_PLAYERTREASURE = "assets/playerTreasure.png"
    SPRITE_TREASURE = "assets/treasure.png"
    SPRITE_SPAWN = "assets/spawn.png"
    CURSOR = "assets/cursor.png"

    SOUND_SHOT = "assets/shot.wav"

    REQUEST_STOP = "stop"
    REQUEST_REGISTER = "register"
    REQUEST_UNREGISTER = "unregister"
    REQUEST_GETMAZE = "getMaze"
    REQUEST_MOVE = "move"
    REQUEST_ROTATE = "rotate"
    REQUEST_SHOOT = "shoot"
    REQUEST_GETUPDATES = "getUpdates"

    PARAM_NAME = "name"
    PARAM_ID = "id"
    PARAM_DIR = "dir"

    RESPONSE_SUCCESS = "success"
    RESPONSE_FAILURE = "failure"

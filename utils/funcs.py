def raycast(maze, pos, dir):
    posX, posY = pos
    dirX, dirY = dir

    x = int(posX)
    y = int(posY)

    if dirX == 0:
        dirX = 0.0000000001
    if dirY == 0:
        dirY = 0.0000000001

    dx = 1.0 / abs(dirX)
    dy = 1.0 / abs(dirY)

    if dirX > 0:
        tx = (x + 1 - posX) * dx
        incX = 1
    else:
        tx = (posX - x) * dx
        incX = -1

    if dirY > 0:
        ty = (y + 1 - posY) * dy
        incY = 1
    else:
        ty = (posY - y) * dy
        incY = -1

    hit = False
    side = "x"
    while not hit:
        if tx < ty:
            tx += dx
            x += incX
            side = "x"
        else:
            ty += dy
            y += incY
            side = "y"

        if maze[y][x] != 0:
            hit = True

    dist = tx - dx if side == "x" else ty - dy

    return dist, side

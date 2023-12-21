from objects.tiles import Tile

class Wall(Tile):
    def __init__(self, board, pos, size, color, imageName = "wall"):
        Tile.__init__(self, board, pos, size, color, imageName = imageName)
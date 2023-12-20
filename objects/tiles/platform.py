from objects.tiles.tile import Tile

class Platform(Tile):
    
    def __init__(self, board, pos, size, color, image = "textures/platform.png"):
        Tile.__init__(self, board, pos, size, color, image = image)
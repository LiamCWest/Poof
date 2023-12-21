from objects.tiles.tile import Tile

class Platform(Tile):
    
    def __init__(self, board, pos, size, color, imageName = "platform"):
        Tile.__init__(self, board, pos, size, color, imageName = imageName)
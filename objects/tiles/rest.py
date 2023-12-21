from objects.tiles.tile import Tile

class Rest(Tile):
    
    def __init__(self, board, pos, size, color, imageName = "rest"):
        Tile.__init__(self, board, pos, size, color, imageName = imageName)
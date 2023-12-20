from objects.tiles.tile import Tile

class Rest(Tile):
    
    def __init__(self, board, pos, size, color, image = "textures/rest.png"):
        Tile.__init__(self, board, pos, size, color, image = image)
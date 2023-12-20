from tile import Tile

class Platform(Tile):
    
    def __init__(self, board, pos, size, color, image = None):
        super.init(board, pos, size, color, image)
class Tile:
    def __init__(self, pos, color, appearedTime = None, disappearedTime = None, type = None):
        self.pos = pos
        self.color = color
        self.appearedTime = appearedTime
        self.disappearedTime = disappearedTime
        self.type = type
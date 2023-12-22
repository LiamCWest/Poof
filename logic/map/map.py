from objects.board import Board

class MapEvent:
    def __init__(self, tile, appearedTime, disappearedTime):
        self.tile = tile
        self.appearedTime = appearedTime
        self.disappearedTime = disappearedTime

class Map():
    def __init__(self, events, appearTime, disappearTime):
        self.events = events
        self.appearTime = appearTime
        self.disappearTime = disappearTime
        
from objects.gameObject import GameObject

class Tile(GameObject):
    def __init__(self, x, y, size, color, image = None):
        super().__init__(x, y, size, size, color, image)
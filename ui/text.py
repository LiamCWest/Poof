import graphics.gui as gui

class Text:
    def __init__(self, text, x, y, color = (0, 0, 0), size = 25, font = "Arial", z = 0):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.size = size
        self.scale = 1
        self.factor = 1
        self.z = z

    def draw(self, cutOff = None):
        gui.drawText(self.text, self.x * self.factor, self.y * self.factor, int(self.size * self.factor * self.scale), self.color, self.font, cutOff)
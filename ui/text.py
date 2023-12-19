import graphics.gui as gui

class Text:
    def __init__(self, text, x, y, color, size, font = "Arial"):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = font
        self.size = size

    def draw(self):
        gui.drawText(self.text, self.x, self.y, self.size, self.color, self.font)
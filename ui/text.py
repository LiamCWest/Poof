import graphics.gui as gui
from utils.vector2 import Vector2

import pygame

class Text:
    def __init__(self, text, x, y, color = (0, 0, 0), size = 25, font = "Arial", bgColor = None, width = 0, height = 0, z = 0):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.bgColor = bgColor
        self.width = width
        self.height = height
        self.font = font
        self.size = size
        self.scale = 1
        self.factor = 1
        self.z = z

    def getRect(self, pos):
        font = pygame.font.SysFont(self.font, self.size)
        text_surface = font.render(self.text, True, self.color)
        return text_surface.get_rect(center=(self.x+pos.x, self.y+pos.y))

    def draw(self, cutOff = None, pos = Vector2(0, 0), win = None):
        if self.bgColor and win:
            pygame.draw.rect(win, self.bgColor, self.getRect(pos) if self.width == 0 or self.height == 0 else (pos.x, pos.y, self.width, self.height))
        gui.drawText(self.text, self.x * self.factor + pos.x, self.y * self.factor + pos.y, int(self.size * self.factor * self.scale), self.color, self.font, cutOff)
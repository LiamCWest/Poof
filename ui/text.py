# external imports
import pygame

# internal imports
import graphics.gui as gui
from utils.vector2 import Vector2

class Text:
    def __init__(self, text, x, y, color=(0, 0, 0), size=25, bgColor=None, width=0, height=0, z=0, font = "ROG"):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.bgColor = bgColor
        self.width = width
        self.height = height
        self.size = size
        self.scale = 1
        self.z = z
        self.lines = text.split('\n')  # Split text into lines
        self.font = font

    def getRect(self, pos):
        font = pygame.font.SysFont(self.font, self.size)
        text_height = font.size(self.text)[1] * len(self.lines)  # Calculate total text height
        return pygame.Rect(self.x + pos.x, self.y + pos.y, self.width, text_height)

    def draw(self, cutOff=None, pos=Vector2(0, 0), win=None):
        self.lines = self.text.split('\n')
        if self.bgColor and win:
            pygame.draw.rect(win, self.bgColor, self.getRect(pos) if self.width == 0 or self.height == 0 else (pos.x, pos.y, self.width, self.height))

        lineHeight = self.size #please
        
        totalHeight = lineHeight * len(self.lines)
        for i, line in enumerate(self.lines):
            y_offset = self.y + pos.y - totalHeight/2 + lineHeight/2 + i * lineHeight  # Calculate y position for each line
            gui.drawText(line, self.x + pos.x, y_offset, int(self.size * self.scale), self.color, self.font, cutOff)
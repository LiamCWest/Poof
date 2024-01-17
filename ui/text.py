#represents text on screen

# external imports
import pygame #import the pygame module

# internal imports
import graphics.gui as gui #import the graphics module
from utils.vector2 import Vector2 #import the vector2 class

class Text: #create a displayable text object
    def __init__(self, text, x, y, color=(0, 0, 0), size=25, bgColor=None, width=0, height=0, z=0, font = "ROG", outlineColor = (0,0,0), outlineSize = 0): #initialize the text
        self.text = text #set the message of the text
        self.x = x #set the x position
        self.y = y #set the y position
        self.color = color #set the color of the text
        self.bgColor = bgColor #set the color of the background (if needed)
        self.width = width #set the width of the text shape
        self.height = height #set the height of the text shape
        self.size = size #set the size of the text
        self.scale = 1 #set the scale of the text
        self.z = z #set the z of the text
        self.lines = text.split('\n')  # Split text into lines
        self.font = font #set the font of the text
        self.outlineColor = outlineColor #set the outline color of the text
        self.outlineSize = outlineSize #set the outline size of the text

    def getRect(self, pos): #get the rectangular size of the text
        font = pygame.font.SysFont(self.font, self.size) #locate and initialize the font
        text_height = font.size(self.text)[1] * len(self.lines)  # Calculate total text height
        return pygame.Rect(self.x + pos.x, self.y + pos.y, self.width, text_height) #create and return the rectangle of the text size

    def draw(self, cutOff=None, pos=Vector2(0, 0), win=None): #draw the text object
        self.lines = self.text.split('\n') #split text into lines
        if self.bgColor and win: #if there is a background color:
            pygame.draw.rect(win, self.bgColor, self.getRect(pos) if self.width == 0 or self.height == 0 else (pos.x, pos.y, self.width, self.height)) #draw the background

        lineHeight = self.size #set the height of each line
        
        totalHeight = lineHeight * len(self.lines) #get the total height of the text
        for i, line in enumerate(self.lines): #for each line
            y_offset = self.y + pos.y - totalHeight/2 + lineHeight/2 + i * lineHeight  # Calculate y position for each line
            gui.drawText(line, self.x + pos.x, y_offset, int(self.size * self.scale), self.color, self.font, cutOff, self.outlineColor, self.outlineSize) #draw each line of text
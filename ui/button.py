import pygame

from graphics import gui

class Button:
    def __init__(self, text, x, y, width, height, color, textColor, onClick):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.scale = 1
        self.scaler = 1.5
        
        self.textColor = textColor
        self.onClick = onClick
    
    def draw(self):
        x = self.x - (self.width * (self.scale - 1) / 2)
        y = self.y - (self.height * (self.scale - 1) / 2)
        width = self.width * self.scale
        height = self.height * self.scale
        pygame.draw.rect(gui.screen, self.color, (x, y, width, height))
        gui.drawText(self.text, x+width//2, y+height//2, int(20*self.scale), self.textColor)
    
    def update(self):
        self.draw()
        cursorPos = pygame.mouse.get_pos()
        if self.x < cursorPos[0] < self.x + self.width and self.y < cursorPos[1] < self.y + self.height:
            self.scale = self.scaler
        else:
            self.scale = 1
    
    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            cursorPos = pygame.mouse.get_pos()
            if self.x < cursorPos[0] < self.x + self.width and self.y < cursorPos[1] < self.y + self.height:
                self.onClick()
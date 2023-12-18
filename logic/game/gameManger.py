import pygame

import graphics.gui as gui

def init(self):
    pygame.init()
    gui.init()

def gameLoop(self):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            self.handleEvent(event)
        self.update()

def start(self):
    self.gameLoop()

def update(self):
    pass

def handleEvent(self, event):
    self.gui.activeScreen.handleEvent(event)
import pygame

import graphics.gui as gui

def init():
    pygame.init()
    gui.init()

def gameLoop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            handleEvent(event)
        update()

def start():
    gameLoop()

def update():
    gui.update()
    pygame.display.update()

def handleEvent(event):
    gui.handleEvent(event)
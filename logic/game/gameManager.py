import pygame

import graphics.gui as gui
from input import input
from images import images

def init():
    pygame.init()
    gui.init()
    images.init()
    input.init()

def gameLoop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            input.handleEvent(event)
        update()

def start():
    gameLoop()

def update():
    gui.update()
    pygame.display.update()
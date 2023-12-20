import pygame

import graphics.gui as gui
import input.input as input

def init():
    pygame.init()
    gui.init()
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
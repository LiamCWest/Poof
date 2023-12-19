from graphics import gui
from graphics.board import Board
from utils.vector2 import Vector2
import pygame
    
def show():
    gui.setScreen("game")
    gui.clear()
    
def update():
    pass

def draw():
    global board
    board.draw(gui.screen)

def handleEvent(event):
    if event.type == pygame.KEYDOWN:
        key = pygame.key.name(event.key)
        if key in keybinds:
            keybinds[key]()
        else:
            print(key)

board = Board(Vector2(0, 0), Vector2(12, 10), 50, (0, 0, 0))

keybinds = {
    "w": lambda: board.move(Vector2(0, 1)),
    "a": lambda: board.move(Vector2(1, 0)),
    "s": lambda: board.move(Vector2(0, -1)),
    "d": lambda: board.move(Vector2(-1, 0)),
}
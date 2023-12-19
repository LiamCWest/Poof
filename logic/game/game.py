from graphics import gui
from graphics.board import Board
from objects.player import Player
from utils.vector2 import Vector2
import pygame
    
def show():
    gui.setScreen("game")
    gui.clear()
    
def update():
    board.update()

def draw():
    global board
    board.draw(gui.screen)
    player.draw(gui.screen)

def handleEvent(event):
    if event.type == pygame.KEYDOWN:
        key = pygame.key.name(event.key)
        if key in keybinds:
            keybinds[key]()
        else:
            print(key)

board = Board(Vector2(0, 0), Vector2(24, 20), 50, (25, 25, 25))
player = Player(board, Vector2(5, 4), 50, image = "player.png")

keybinds = {
    "w": lambda: board.move(Vector2(0, 1)),
    "a": lambda: board.move(Vector2(1, 0)),
    "s": lambda: board.move(Vector2(0, -1)),
    "d": lambda: board.move(Vector2(-1, 0)),
}
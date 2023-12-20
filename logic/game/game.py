from graphics import gui
from graphics.board import Board
from objects.player import Player
from utils.vector2 import Vector2
import input.input as input
import pygame
    
def show():
    gui.setScreen("game")
    gui.clear()

def checkInput():
    if input.keybinds["left"].justPressed:
        board.move(Vector2(1, 0))
    
    if input.keybinds["right"].justPressed:
        board.move(Vector2(-1, 0))
        
    if input.keybinds["up"].justPressed:
        board.move(Vector2(0, 1))
        
    if input.keybinds["down"].justPressed:
        board.move(Vector2(0, -1))
    
def update():
    checkInput()
    board.update()

def draw():
    global board
    board.draw(gui.screen)
    player.draw(gui.screen)

def handleEvent(event):
    pass

board = Board(Vector2(0, 0), Vector2(24, 20), 50, (25, 25, 25))
player = Player(board, Vector2(5, 4), 50, image = "player.png")
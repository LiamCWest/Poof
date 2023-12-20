from graphics import gui
from graphics.board import Board
from objects.player import Player
from graphics.particleSystem.emitter import ParticleEmitter
from utils.vector2 import Vector2
import input.input as input
import pygame
    
def show():
    gui.setScreen("game")
    gui.clear()

def checkInput():
    if input.keyBindings["left"].justPressed:
        board.move(Vector2(1, 0))
    
    if input.keyBindings["right"].justPressed:
        board.move(Vector2(-1, 0))
        
    if input.keyBindings["up"].justPressed:
        board.move(Vector2(0, 1))
        
    if input.keyBindings["down"].justPressed:
        board.move(Vector2(0, -1))
    
def update():
    checkInput()
    board.update()

def draw():
    global board, player
    board.draw(gui.screen)
    player.draw(gui.screen)

def addBaseObjects():
    global board, player
    board = Board(Vector2(0, 0), Vector2(24, 20), 50, (25, 25, 25))
    player = Player(board, Vector2(5, 4), 50)
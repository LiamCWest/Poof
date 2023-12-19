import pygame

from ui import mainMenu
from logic.game import game

def init():
    global screen, screens, activeScreen, activeScreenName
    screen = pygame.display.set_mode((640, 480))
    screen.fill((255, 255, 255))
    
    screens = {"main": mainMenu, "game": game}
    screens["main"].show()
    
def setScreen(name):
    global activeScreen, activeScreenName
    activeScreenName = name
    activeScreen = screens[activeScreenName] if activeScreenName != "none" else None

def drawText(text, x, y, size, color):
    global screen
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    
def clear():
    global screen
    screen.fill((55, 55, 55))
    
def update():
    global activeScreen
    if activeScreen: activeScreen.update()
    draw()
    
def draw():
    global activeScreen
    clear()
    if activeScreen: activeScreen.draw()
    
def handleEvent(event):
    global activeScreen
    if activeScreen: activeScreen.handleEvent(event)
import pygame

from ui.menus import mainMenu, settingsMenu
from logic.game import game

screen = None
screens = None
activeScreen = None
activeScreenName = None
def init():
    global screen, screens, activeScreen, activeScreenName
    screen = pygame.display.set_mode((640, 480))
    screen.fill((255, 255, 255))
    
    screens = {"main": mainMenu, "game": game, "settings": settingsMenu}
    setScreen("main")

def setScreen(name):
    global activeScreen, activeScreenName
    
    if activeScreen:
        activeScreen.hide()
    
    activeScreenName = name
    activeScreen = screens[activeScreenName]
    
    activeScreen.show()

def drawText(text, x, y, size, color, font = "Arial"):
    global screen
    font = pygame.font.SysFont(font, size)
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
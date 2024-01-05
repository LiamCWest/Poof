import pygame

from ui.menus import mainMenu, settingsMenu, levelMenu
import logic.level.levelEditor as levelEditor
from logic.game import game

screen = None
screens = None
activeScreen = None
activeScreenName = None
def init():
    global screen, screens, activeScreen, activeScreenName
    screen = pygame.display.set_mode((1280, 720))
    screen.fill((255, 255, 255))
    
    screens = {"main": mainMenu, "game": game, "settings": settingsMenu, "levelEditor": levelEditor, "levelMenu": levelMenu}
    setScreen("main")

def setScreen(name):
    global activeScreen, activeScreenName
    
    if activeScreen:
        activeScreen.hide()
    
    activeScreenName = name
    activeScreen = screens[activeScreenName]
    
    activeScreen.show()

def drawText(text, x, y, size, color, font = "Arial", cutOff = None):
    global screen
    font = pygame.font.SysFont(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))

    if cutOff:
        cutOff_rect = pygame.Rect(cutOff)
        if text_rect.colliderect(cutOff_rect):
            cutOff_surface = screen.subsurface(cutOff_rect)
            cutOff_surface.blit(text_surface, text_rect.move(-cutOff_rect.topleft[0], -cutOff_rect.topleft[1]))
    else:
        screen.blit(text_surface, text_rect)
    
def clear():
    global screen
    screen.fill((55, 55, 55))
    
def update():
    global activeScreen
    #factor = resizeFactor()
    if activeScreen: 
        #activeScreen.updateFactors(factor)
        activeScreen.update()
    draw()
    
def resizeFactor():
    global screen
    factor = min(screen.get_width()/1280, screen.get_height()/720)
    return factor
    
def draw():
    global activeScreen
    clear()
    if activeScreen: activeScreen.draw()
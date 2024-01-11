import pygame
import ctypes
import platform

from ui.menus import mainMenu, settingsMenu, levelMenu
import logic.level.levelEditor as levelEditor
from logic.game import game
from utils.stack import Stack
import input.input as input
from fonts.fonts import getFont

screen = None
screens = None
activeScreen = None
activeScreenName = None
screenStack = Stack()
def init():
    if platform.system() == "Windows": ctypes.windll.user32.SetProcessDPIAware() #makes window not scale with display scaling
    
    global screen, screens, activeScreen, activeScreenName
    screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
    screen.fill((255, 255, 255))
    
    screens = {"main": mainMenu, "game": game, "settings": settingsMenu, "levelEditor": levelEditor, "levelMenu": levelMenu}
    setScreen("main")

def setScreen(name, back = False):
    global activeScreen, activeScreenName, screenStack
    
    if activeScreen:
        activeScreen.hide()
    
    if not back: screenStack.push(activeScreenName)
    activeScreenName = name
    activeScreen = screens[activeScreenName]
    
    activeScreen.show()

def back():
    global screenStack
    if screenStack.peek: setScreen(screenStack.pop(), back = True)

def checkInput():
    if input.specialKeyBindings["escape"].justPressed:
        if activeScreenName not in ["game", "main"]:
            if activeScreen.popupOpen:
                activeScreen.popupClose()
            else:
                back()
        elif activeScreenName == "game":
            if activeScreen.popupOpen:
                activeScreen.resume()
            else:
                activeScreen.pause()

def drawText(text, x, y, size, color, font, cutOff = None):
    global screen
    text_surface = getFont(font, size).render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))

    if cutOff:
        cutOff_rect = pygame.Rect(cutOff).clip(screen.get_rect())
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
    checkInput()
    if activeScreen: 
        activeScreen.update()
    draw()
    
def draw():
    global activeScreen
    clear()
    if activeScreen: activeScreen.draw()
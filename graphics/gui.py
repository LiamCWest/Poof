#the module that handles screen manipulation, as well as drawing text for some reason

# external imports
import pygame #import the pygame module
import ctypes #import the ctypes module
import platform #import the platform module

# internal imports
import logic.level.levelEditor as levelEditor #import the level editor
import input.input as input #import the input system
from logic.game import game #import the game loop system
from utils.stack import Stack #import the stack class
from fonts.fonts import getFont #import the getFont class
from ui.menus import mainMenu, settingsMenu, levelMenu #import the various menu classes

screen = None #default the screen to none
screens = None #default the screen list to none
activeScreen = None #default the active screen to none
activeScreenName = None #default the name of the active screen to none
screenStack = Stack() #create an empty stack for the screens
def init(): #initialize the GUI system
    if platform.system() == "Windows": ctypes.windll.user32.SetProcessDPIAware() #makes window not scale with display scaling
    
    global screen, screens, activeScreen, activeScreenName #move these variables to the global scope
    screen = pygame.display.set_mode((1280, 720), pygame.SCALED) #create the diplay screen
    screen.fill((255, 255, 255)) #fill the screen with a white background
    
    screens = {"main": mainMenu, "game": game, "settings": settingsMenu, "levelEditor": levelEditor, "levelMenu": levelMenu} #create screens for the menus
    setScreen("main") #set the screen to the main menu

def setScreen(name, back = False): #this sets the screen to the inputted screen
    global activeScreen, activeScreenName, screenStack #move these variables to the global scope
    
    if activeScreen: #if there is an active screen
        activeScreen.hide() #hide the active screen
    
    if not back: screenStack.push(activeScreenName) #if not moving back, add the screen to the stack
    activeScreenName = name #set the active screen name to the name of the screen
    activeScreen = screens[activeScreenName] #set the active screen
    
    activeScreen.show() #show the active screen

def back(): #this handles moving backwards in the screen stack
    global screenStack #move screenStack to the global scope
    if screenStack.peek: setScreen(screenStack.pop(), back = True) #if the screen stack isn't empty, pop the current screen and set the new screen

def checkInput(): #handle various inputs
    if input.specialKeyBindings["escape"].justPressed: #if escape key is pressed
        if activeScreenName not in ["game", "main"]: #and the active screen isn't "game" or "main" (the player isn't mid-game or on the main menu)
            if activeScreen.popupOpen: #if the active screen has a popup open
                activeScreen.popupClose() #close the popup
            else: #if the active screen doesn't have a popup open
                back() #move the active screen back in the screen stack
        elif activeScreenName == "game": #if the active screen is the game window
            if activeScreen.popupOpen: #if the active screen has a popup open
                activeScreen.resume() #close the popup and resume gameplay
            else: #if there is no current popup
                activeScreen.pause() #pause the game and create the pause popup

def drawText(text, x, y, size, color, font, cutOff = None): #this function draws text to the screen
    global screen #get the screen from the global scope
    text_surface = getFont(font, size).render(text, True, color) #create a new surface for the text font
    text_rect = text_surface.get_rect(center=(x, y)) #create the rectangle that contains the text

    if cutOff: #if the text will be cut off
        cutOff_rect = pygame.Rect(cutOff).clip(screen.get_rect()) #clip the part of the screen that will be cut off
        if text_rect.colliderect(cutOff_rect): #if the text collides with the cut off part
            cutOff_surface = screen.subsurface(cutOff_rect) #create a new surface for the new cutOff surface
            cutOff_surface.blit(text_surface, text_rect.move(-cutOff_rect.topleft[0], -cutOff_rect.topleft[1])) #blit the cut off surface
    else: #if the text is not cut off
        screen.blit(text_surface, text_rect) #blit the text onto the screen
    
def clear(): #clears the screen
    global screen #retrieve the screen from globals
    screen.fill((55, 55, 55)) #fill the screen with dark grey
    
def update(): #updates the screen
    global activeScreen #retrieve the active screen from globals
    checkInput() #check and handle input events
    if activeScreen: #if there is an active screen
        activeScreen.update() #update the active screen
    draw() #draw the entire screen
    
def draw(): #draws the screen
    global activeScreen #retrieve the active screen from globals
    clear() #clear the game window
    if activeScreen: activeScreen.draw() #draw the screen if it exists
#the main menu of the game

# external imports
from copy import deepcopy #importy the deepcopy function

# internal imports
from ui.button import Button #import the button class
from ui.text import Text #import the text class
from ui.scrollbar import Scrollbar #import the scrollbar class
from ui.menus import levelMenu #import the level menu object
from ui.inputBox import InputBox #import the input box class
from logic.level import levelEditor as LE #import the level editor
from logic.game import game #import the game system
from utils.vector2 import Vector2 #import the vector2 class
from graphics import gui #import the graphics system
from graphics.particleSystem.toggleableEmitter import ToggleableShapedEmitter #import the toggleable shaped emitter class

def show(): #shows the screen
    gui.clear() #clear the window
    update() #update objects on the screen

def hide(): #hides the screen
    gui.clear() #clear the screen

def draw(): #draws all objects on the screen
    for object in objects: #for each object in the menu
        object.draw(gui.screen) #draw the object
    for text in texts: #for each text in the menu
        text.draw() #draw the text

def startGame(): #starts the game and loads the level
    levelMenu.start(lambda level: load(level)) #opens the levelmenu and loads all levels
    gui.setScreen("levelMenu") #sets the screen to the level select menu
    def load(level): #loads the inputted level
        game.loadLevel(level) #load the inputted level
        gui.setScreen("game") #set the screen to the game screen
        
def update(): #updtates all objects in the menu
    for object in objects: #for each object
        object.update() #update the object
        
def settings(): #opens the settings menu
    gui.setScreen("settings") #set the screen to the settings menu
    
def levelEditor(): #initializes the level editor
    levelMenu.start(lambda level: load(level), isLevelEditor=True) #open the level menu
    gui.setScreen("levelMenu") #set the screen to the level menu
    def load(level): #loads the inputted level
        LE.loadLevel(level) #load the inputted level
        gui.setScreen("levelEditor") #set the screen to the level editor
        
title = "Main Menu" #set the title of the menu to "Main Menu"
emitter = ToggleableShapedEmitter(None, None, Vector2(4,4), 250, 25, 10, edges = "V") #create a reusable emitter for all the buttons
objects = [Button("Start", 200, 200, 880, 100, (80, 93, 112), (255, 255, 255), onRelease=startGame, particles=deepcopy(emitter), textFont= "ROG", particlesOnOver=True, scaler = 1.05), #create the start button
           Button("Settings", 200, 320, 880, 100, (80, 93, 112), (255, 255, 255), onRelease=settings, particles=deepcopy(emitter), textFont= "ROG", particlesOnOver=True, scaler = 1.05), #settings button
           Button("Level Editor", 200, 440, 880, 100, (80, 93, 112), (255, 255, 255), onRelease=levelEditor, particles=deepcopy(emitter), textFont= "ROG", particlesOnOver=True, scaler = 1.05), #level editor button
           Button("Quit", 200, 560, 880, 100, (80, 93, 112), (255, 255, 255), onRelease=quit, particles=deepcopy(emitter), textFont= "ROG", particlesOnOver=True, scaler = 1.05),] #quit the game
texts = [Text(title, 640, 100, (255, 255, 255), 100, font= "ROG")] #create a text object for the title
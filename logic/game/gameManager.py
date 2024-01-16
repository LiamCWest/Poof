#the module that handles the main game loop and initialization of everything

# external imports
import pygame 

# internal imports
import graphics.gui as gui #for drawing
from input import input #for input handling
from images import images #for loading images

def init(): #initializes the game
    pygame.init() #initialize pygame
    gui.init() #initialize the gui
    images.init() #initialize the images
    input.init() #initialize the input

def gameLoop(): #the main game loop
    while True: #loop forever
        for event in pygame.event.get(): #for every pygame event
            if event.type == pygame.QUIT: #if the user tries to quit
                pygame.quit() #quit pygame
                quit() #quit python
            input.handleEvent(event) #else handle the event
        update() #update the game

def start(): #starts the game
    gameLoop() #start the game loop

def update(): #updates the game
    input.updateFrameTimes() #update the frame times in input
    
    gui.update() #update the gui
    pygame.display.update() #update pygame
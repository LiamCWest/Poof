#the main file, where everything starts

#external imports
import pygame

# internal imports
import graphics.gui as gui #for drawing
from input import input #for input handling
from images import images #for loading images

def main(): # main function, where everything starts
    init() # initialize
    while True: #loop forever
        for event in pygame.event.get(): #for every pygame event
            if event.type == pygame.QUIT: #if the user tries to quit
                pygame.quit() #quit pygame
                quit() #quit python
            input.handleEvent(event) #else handle the event
        update() #update the game

def update(): #updates the game
    input.updateFrameTimes() #update the frame times in input
    
    gui.update() #update the gui
    pygame.display.update() #update pygame

def init(): #initializes the game
    pygame.init() #initialize pygame
    gui.init() #initialize the gui
    images.init() #initialize the images
    input.init() #initialize the input

if __name__ == "__main__": # if this file is being run directly
    main() # run the main function



### OLD ASYNC VERSION OF MAIN.PY FROM WHEN WE WERE TRYING TO USE PYGBAG ###
'''#the main file, where everything starts

#external imports
import pygame
import asyncio

# internal imports
import graphics.gui as gui #for drawing
from input import input #for input handling
from images import images #for loading images

async def main(): # main function, where everything starts
    init() # initialize
    while True: #loop forever
        for event in pygame.event.get(): #for every pygame event
            if event.type == pygame.QUIT: #if the user tries to quit
                pygame.quit() #quit pygame
                quit() #quit python
            input.handleEvent(event) #else handle the event
        update() #update the game
        await asyncio.sleep(0) #wait for a frame

def update(): #updates the game
    input.updateFrameTimes() #update the frame times in input
    
    gui.update() #update the gui
    pygame.display.update() #update pygame

def init(): #initializes the game
    pygame.init() #initialize pygame
    gui.init() #initialize the gui
    images.init() #initialize the images
    input.init() #initialize the input

# if __name__ == "__main__": # if this file is being run directly
asyncio.run(main()) # run the main function'''
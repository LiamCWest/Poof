#draws a debug texture. unused by the game

# external imports
import pygame as pg # for drawing to the screen

def verifyTexture(filename): # verifies that a texture exists
    try: # try to open the texture
        open(filename) # open the texture
        out = filename # set the output to the filename
    except: # if the texture does not exist
        out = createDebugTexture("textures/debug.png") # create a debug texture
    return out # return the output

def createDebugTexture(filename, size = 8, c1 = (0,0,0), c2 = (255,0,255)): # creates a debug texture
    
    try: # try to open the texture
        open(filename) # open the texture
        
    except: # if the texture does not exist
        surface = pg.Surface((size,size)) # create a surface

        half = size / 2 # half the size
        pg.draw.rect(surface,c1,(0,0,size,size)) # draw a big black rectangle
        
        pg.draw.rect(surface,c2,(half,0,half,half)) # draw a small pink rectangle
        pg.draw.rect(surface,c2,(0,half,half,half)) # draw a small pink rectangle
        
        pg.image.save(surface, filename) # save the surface to the filename
        
        try: # try to open the texture
            open(filename) # open the texture
             
        except: # if the texture does not exist
            print("Error creating debug texture") # print an error message
            
    return filename # return the filename of the texture
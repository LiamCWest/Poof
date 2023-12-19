import pygame as pg

def verifyTexture(filename):
    try:
        open(filename)
        out = filename
    except:
        out = createDebugTexture("debug.png")
    return out

def createDebugTexture(filename, size = 8, c1 = (0,0,0), c2 = (255,0,255)):
    
    try:
        open(filename)
        
    except:
        surface = pg.Surface((size,size))

        half = size / 2
        pg.draw.rect(surface,c1,(0,0,size,size))
        
        pg.draw.rect(surface,c2,(half,0,half,half))
        pg.draw.rect(surface,c2,(0,half,half,half))
        
        pg.image.save(surface, filename)
        
        try:
            open(filename)
            
        except:
            print("Error creating debug texture")
            
    return filename
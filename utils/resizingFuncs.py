import pygame

def blitResized(surface, image, pos, size, factor):
    size *= factor
    surface.blit(pygame.transform.scale(image, (size,size)), (pos.x*size, pos.y*size))

def drawRectResized(surface, color, x, y, width, height, factor):
    pygame.draw.rect(surface, color, (x*factor, y*factor, width*factor, height*factor))

#def drawRectResized(x, y, width, height, factor):
    
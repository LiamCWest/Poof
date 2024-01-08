import pygame

def blitResized(surface, image, pos, size, factor, scale):
    size *= factor
    pos = pos.multiply(size)
    surface.blit(pygame.transform.scale(image, (scale,scale)), (pos.x - scale/2, pos.y - scale/2))

def drawRectResized(surface, color, x, y, width, height, factor):
    rect = (x*factor, y*factor, width*factor, height*factor)
    pygame.draw.rect(surface, color, rect)
    return rect

#def drawRectResized(x, y, width, height, factor):
    
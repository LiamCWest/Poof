import pygame

from ui import mainMenu

def init(self):
    self.screen = pygame.display.set_mode((640, 480))
    self.screen.fill((255, 255, 255))
    
    self.menus = {"main": mainMenu}
    self.menus("main").show()
    
def drawText(self, text, x, y, size, color):
    font = pygame.font.SysFont("comicsansms", size)
    text = font.render(text, True, color)
    self.screen.blit(text, (x, y))
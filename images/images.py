import pathlib
import pygame.image as image
texturePath = pathlib.Path(__file__).parent

def loadImage(name):
    global texturePath
    imagePath = texturePath/name
    return image.load(str(imagePath)).convert()

images = {
    "debug": None,
    "platform": None,
    "player": None,
    "rest": None
}

def init():
    global images
    print("initiated")
    images["debug"] = loadImage("debug.png")
    images["platform"] = loadImage("platform.png")
    images["player"] = loadImage("player.png")
    images["rest"] = loadImage("rest.png")
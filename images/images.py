import pathlib
import pygame.image as image
texturePath = pathlib.Path(__file__).parent

def loadImage(name):
    global texturePath
    imagePath = texturePath/name
    return image.load(str(imagePath)).convert_alpha()

images = {
    "debug": None,
    
    "platform": None,
    
    "player_left": None,
    "player_up": None,
    "player_right": None,
    "player_down": None,
    "player_left_moving": None,
    "player_up_moving": None,
    "player_right_moving": None,
    "player_down_moving": None,
    
    "rest": None
}

def init():
    global images
    images["debug"] = loadImage("debug.png")
    images["platform"] = loadImage("platform.png")
    
    images["player_left"] = loadImage("player/player_left.png")
    images["player_up"] = loadImage("player/player_up.png")
    images["player_right"] = loadImage("player/player_right.png")
    images["player_down"] = loadImage("player/player_down.png")
    images["player_left_moving"] = loadImage("player/player_left_moving.png")
    images["player_up_moving"] = loadImage("player/player_up_moving.png")
    images["player_right_moving"] = loadImage("player/player_right_moving.png")
    images["player_down_moving"] = loadImage("player/player_down_moving.png")
    
    images["rest"] = loadImage("rest.png")
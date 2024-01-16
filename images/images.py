#a module that stores all the images used in the game in one easy location

# external imports
import pathlib # for manipulating file paths
import pygame.image as image # for loading images

imagesPath = pathlib.Path(__file__).parent # get the path to the images folder

def loadImage(name): # loads an image
    global imagesPath # globals
    imagePath = imagesPath/name # get the path to the image
    return image.load(str(imagePath)).convert_alpha() # load the image, convert it so its faster, and return it

images = { # a dictionary of all the images
    "debug": None, # the debug texture (not used in the game)
    
    "platform": None, # the platform tile texture
    "glide": None, # the glide tile texture
    "glidePath": None, #the glide path tile texture
    "rest": None, # the rest tile texture
    
    "player_left": None, # the player texture facing left
    "player_up": None, # the player texture facing up
    "player_right": None, # the player texture facing right
    "player_down": None, # the player texture facing down
    "player_left_moving": None, # the player texture facing left while moving
    "player_up_moving": None, # the player texture facing up while moving
    "player_right_moving": None, # the player texture facing right while moving
    "player_down_moving": None, # the player texture facing down while moving
}

def init(): # initializes the images
    global images # globals
    images["debug"] = loadImage("debug.png") # load the debug texture
    images["platform"] = loadImage("platform.png") # load the platform texture
    images["glide"] = loadImage("glide.png") # load the glide texture
    images["glidePath"] = loadImage("glidePath.png") # load the glide path texture
    images["rest"] = loadImage("rest.png") # load the rest texture
    
    images["player_left"] = loadImage("player/player_left.png") # load the player texture facing left
    images["player_up"] = loadImage("player/player_up.png") # load the player texture facing up
    images["player_right"] = loadImage("player/player_right.png") # load the player texture facing right
    images["player_down"] = loadImage("player/player_down.png") # load the player texture facing down
    images["player_left_moving"] = loadImage("player/player_left_moving.png") # load the player texture facing left while moving
    images["player_up_moving"] = loadImage("player/player_up_moving.png") # load the player texture facing up while moving
    images["player_right_moving"] = loadImage("player/player_right_moving.png") # load the player texture facing right while moving
    images["player_down_moving"] = loadImage("player/player_down_moving.png") # load the player texture facing down while moving
#the level select menu of the game

# external imports
import os #for getting the level files

# internal imports
from ui.button import Button #for buttons
from ui.popup import Popup #for popups
from ui.inputBox import InputBox #for input boxes
from ui.text import Text #for text
from utils.vector2 import Vector2 #for vectors
from logic.level.level import Level #for levels
from logic.song.timingPoints import TimeSignature, TimingPoint #for timing points
from objects.tile import Tile #for tiles
from graphics import gui #for drawing
from graphics.particleSystem.shapedEmitter import ShapedEmitter #for particles
from logic.level import levelEditor as LE #for loading levels

# list of popup objects
popups = []

#shows the level select menu
def show():
    global levels, buttons, popupOpen, popups #get the global variables
    # if the menu is directed at the level editor, add a new level button
    if isLE: buttons.append(Button("New Level", gui.screen.get_width()/2-150, 500, 300, 50, (255,0,0), (0,0,0), onRelease=newLevel))
    # else, reset buttons
    else: buttons = []
    levels = getLevels("levels") #get the levels
    levelButtons = [] #create a list of buttons for each level
    for i, level in enumerate(levels): #for each level
        levelButtons.append(genLevelButton(level, i)) #add a button for the level
    buttons += levelButtons #add the level buttons to the buttons list
    
    popupOpen = False #set the popup to closed
    nLW = 500 #new level popup width
    genericParticles = ShapedEmitter(None, None, Vector2(2,2), 750, 15, 5) #create a particle emitter for the popup
    popups = { #create the popups
        "newLevel": Popup(Vector2((1280-nLW)/2, 0), nLW, 650, (0,0,0), None,
                        [
                            InputBox("Level Name", (nLW-400)/2, 150, 400, 50, (80, 93, 112), (255,255,255), 30, scaler = 1.1), # create the level name input box
                            InputBox("Song File", (nLW-400)/2, 225, 400, 50, (80, 93, 112), (255,255,255), 30, scaler = 1.1), # create the song file input box
                            InputBox("Offset", (nLW-400)/2, 325, 175, 50, (80, 93, 112), (255,255,255), 30, numOnly=True, scaler = 1.1), # create the offset input box
                            InputBox("BPM", (nLW-400)/2, 375, 175, 50, (80, 93, 112), (255,255,255), 30, numOnly=True, scaler = 1.1), # create the bpm input box
                            InputBox("Num", (nLW)/2 + 25, 325, 175, 50, (80, 93, 112), (255,255,255), 30, numOnly=True, scaler = 1.1), # create the numerator input box
                            InputBox("Denom", (nLW)/2 + 25, 375, 175, 50, (80, 93, 112), (255,255,255), 30, numOnly=True, scaler = 1.1), # create the denominator input box
                            Button("Create", (nLW-400)/2, 475, 400, 50, (80, 93, 112), (255,255,255), onRelease=createLevel, particles = genericParticles, particlesOnOver = True, scaler = 1.1), # create the create button
                            Button("Close", (nLW-400)/2, 550, 400, 50, (80, 93, 112), (255,255,255), onRelease=popupClose, scaler = 1.1), # create the close button
                         ],
                        [Text("New Level", nLW/2, 75, (255, 255, 255), 60, font = "ROG")]), # create the title text
    }

# sets the varible for going to the level editor to false
isLE = False

# start function
def start(load, isLevelEditor = False):
    global loadLevel, isLE #get the global variables
    loadLevel = load #set the load level function
    isLE = isLevelEditor #set the is level editor variable

# hide function because all menus need one
def hide():
    pass

# update function
def update():
    global buttons, popups, popupOpen #get the global variables
    if not popupOpen: #if there is no popup open
        for button in buttons: #for each button
            button.update() #update the button
    for popup in popups.values(): #for each popup
        popup.update() #update the popup

# draw function
def draw():
    global buttons, popups #get the global variables
    for button in buttons: #for each button
        button.draw(gui.screen) #draw the button
    for popup in popups.values(): #for each popup
        popup.draw() #draw the popup

# gen level button function
def genLevelButton(level, i):
    rowLength = 5 #the number of levels per row
    x = 100 + (i % rowLength) * 200 #the x position of the button
    y = 100 + (i // rowLength) * 150 #the y position of the button
    # return a button for the level
    return Button(getLevelName(level), x, y, 200, 200, (0,0,0), (255,255,255), onRelease=lambda: loadLevel(level), textSize=20)

# open the new level popup
def newLevel():
    global popups, popupOpen #get the global variables
    popupOpen = True #set the popup to open
    popups["newLevel"].show() #show the popup

# create a new level
def createLevel():
    global popups, popupOpen #get the global variables
    levelPopup = popups["newLevel"] #get the new level popup
    if any([inputBox.output != "" for inputBox in levelPopup.objects[:2]]): #if the level name or song file is not empty
        levelName = levelPopup.objects[0].output #get the level name
        song = levelPopup.objects[1].output #get the song file
        offset = float(levelPopup.objects[2].output) #get the offset
        bpm = int(levelPopup.objects[3].output) #get the bpm
        num = int(levelPopup.objects[4].output) #get the numerator
        denom = int(levelPopup.objects[5].output) #get the denominator
        timeSig = TimeSignature(num, denom) #create the time signature
        timingPoint = TimingPoint(offset, bpm, timeSig) #create the timing point
        
        #create the level
        nLevel = Level([Tile(Vector2(0, 0), None, 0, offset, "platform")], 1, 1, song, [timingPoint], Vector2(0,0), 0)
        levelFilePath = "levels/" + levelName + ".json" # set the level file path
        nLevel.save(levelFilePath) #save the level
        LE.loadLevel(levelFilePath) #load the level
        gui.setScreen("levelEditor") #set the screen to the level editor

# close the popups
def popupClose(): 
    global popups, popupOpen #get the global variables
    popupOpen = False #set the popup to closed
    for popup in popups.values(): #for each popup
        if popup.open: popup.hide() #hide the popup

# get the name of a level
def getLevelName(level):
    return os.path.basename(level).split(".")[0] #return the name of the level

# get all levels in a directory
def getLevels(levelDir):
    return [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(levelDir) for f in filenames] #return all levels in a directory

# list of buttons
buttons = []
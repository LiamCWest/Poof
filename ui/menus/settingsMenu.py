# internal imports
from graphics import gui # import gui from graphics
from ui.text import Text # import Text from ui.text
from ui.scrollbar import Scrollbar # import Scrollbar from ui.scrollbar
from logic.song import songPlayer # import songPlayer from logic.song

# show the settings menu
def show():
    gui.clear() # clear the gui
    update() # update the settings menu

# hide the settings menu
def hide():
    gui.clear() # clear the gui

# draw the settings menu
def draw():
    for object in objects: # for every object in objects
        object.draw(gui.screen) # draw the object
    for text in texts: # for every text in texts
        text.draw() # draw the text

# update the settings menu
def update():
    global objects, texts, lastVolumeVal # get the global objects, texts and lastVolumeVal
    texts[2].text = str(int(objects[0].getValue()*100)) + "%" # set the text of the volume text to the volume
    texts[2].x = objects[0].x + objects[0].length + 50 # set the x of the volume text to the x of the scrollbar + the length of the scrollbar + 50
    if objects[0].getValue() != lastVolumeVal: # if the volume scrollbar has changed
        songPlayer.setVolume(objects[0].getValue()) # set the volume of the songPlayer to the value of the scrollbar
    else: # if the volume scrollbar has not changed
        objects[0].setValue(songPlayer.getVolume()) # set the value of the scrollbar to the volume of the songPlayer
    lastVolumeVal = objects[0].getValue() # set the lastVolumeVal to the value of the scrollbar
    for object in objects: # for every object in objects
        object.update() # update the object

lastVolumeVal = 0 # set the lastVolumeVal to 0
title = "Settings Menu" # set the title to "Settings Menu"
objects = [Scrollbar(350, 200, 50, 800, "h")] # set the objects to a scrollbar
texts = [Text(title, 640, 80, (255, 255, 255), 100), Text("Volume", 175, 220, (255, 255, 255), 50), Text("0%", 1190, 220, (255, 255, 255), 30)] # set the texts to a title, a volume text and a volume value text
popupOpen = False # set the popupOpen to False
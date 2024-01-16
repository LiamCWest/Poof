# used only for detecting keycodes for testing, not needed for the game

# external imports
from pynput import keyboard # for detecting keypresses
import time # for sleeping
 
def toKeyStr(key): # converts a key to a string
    global kbListener # globals
    return str(kbListener.canonical(key)) # return the key as a string

def onKeyPress(key): # called when a key is pressed
    print(toKeyStr(key)) # print the key that was pressed

kbListener = keyboard.Listener(on_press=onKeyPress) # create a keyboard listener that calls onKeyPress when a key is pressed
kbListener.start() # start the keyboard listener

time.sleep(999999999999999999999999) # sleep forever so the program doesn't end
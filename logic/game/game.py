#the game screen, where the level is played

# internal imports
import input.input as input #input system
import logic.song.songPlayer as songPlayer #for playing song
from logic.level.level import Level #for loading and interacting with levels
from objects.player import Player #for the player
from ui.text import Text #for displaying text
from ui.popup import Popup #for displaying popups
from ui.button import Button #for buttons
from graphics import gui #for drawing
from utils.vector2 import Vector2 #for positions
from graphics.particleSystem.shapedEmitter import ShapedEmitter #for particles

level = None #the current level
playing = False #whether or not the song is playing
started = False #whether or not the level has been started
playWait = False #whether or not the level should start playing after the pause menu closes
levelF = None #the file path to the level

popups = {} #the popups on the game screen
def init(): #initializes the game screen
    global started, popups, popupOpen, win, won, accText #globals
    won = False #you havent won
    started = True #the level has started
    genericParticles = ShapedEmitter(None, None, Vector2(2,2), 500, 15, 5) #particles for restart and resume buttons
    popupOpen = False #no popups are open
    pW = 500 #the width of the popups
    popups = { #the popups for the game screen
        "pause": Popup(Vector2((1280-pW)/2, 0), pW, 650, (0,0,0), None, #the pause menu
                [Button("Resume", 50, 275, 400, 100, (80, 93, 112), (255, 255, 255), onRelease=resume, particles=genericParticles, particlesOnOver=True, textFont= "ROG", scaler= 1.1), #the resume button
                Button("Main Menu", 50, 387, 400, 100, (80, 93, 112), (255, 255, 255), onRelease=lambda: gui.setScreen("main"), textFont= "ROG", scaler = 1.1), #the main menu button
                Button("Settings", 50, 500, 400, 100, (80, 93, 112), (255, 255 ,255), onRelease=lambda: gui.setScreen("settings"), textFont= "ROG", scaler = 1.1)], #settings button
                [Text("Pause", 250, 80, (255, 255, 255), 100, font= "ROG"),]), #the pause title text
        "win": Popup(Vector2((1280-pW)/2, 0), pW, 650, (0,0,0), None, #the win menu
                [Button("Restart", 50, 275, 400, 100, (80, 93, 112), (255, 255, 255), onRelease=restart, particles=genericParticles, particlesOnOver=True, textFont= "ROG", scaler= 1.1), #the restart button
                Button("Main Menu", 50, 387, 400, 100, (80, 93, 112), (255, 255, 255), onRelease=lambda: gui.setScreen("main"), textFont= "ROG", scaler = 1.1), #the main menu button
                Button("Settings", 50, 500, 400, 100, (80, 93, 112), (255, 255 ,255), onRelease=lambda: gui.setScreen("settings"), textFont= "ROG", scaler = 1.1)], #the settings button
                [Text("You Win!", 250, 80, (255, 255, 255), 80, font= "ROG"), #the win title text
                 Text("", 250, 191, (255, 255, 255), 40, font= "ROG"),]), #the accuracy and offset text
    }

def show(): #shows the game screen
    global level, started, popupOpen #globals
    if not started: #if the level hasn't been started
        init() #initialize the game screen
    if not popupOpen: play() #if no popups are open, play the level

def restart(): #restarts the level
    global levelF #globals
    popupClose() #close all popups
    loadLevel(levelF) #load level at level file
    play() #play the level

def hide(): #hides the game screen
    gui.clear() #clear the screen

endTime = None #the time the level ends
endPositions = None #the positions the player can be on when the level ends to win
def loadLevel(levelFile): #loads the level at the given file path
    global level, endTime, endPositions, levelF #globals
    levelF = levelFile #set the level file
    songPlayer.unload() #unload the song if there was one playing before
    init() #initialize the game screen
    level = Level.fromFile(levelFile) #load the level
    endTime = level.getEndTime() #get the end time of the level
    endPositions = level.getEndPositions() #get the end positions of the level

def checkInput(): #check input
    if input.keyActionBindings["left"].justPressed: #if you have tried to move left
        level.player.move(Vector2(-1, 0), input.keyActionBindings["left"].songTimeLastPressed) #move left
    elif input.keyActionBindings["left"].justReleased: #if you have stopped trying to move left
        level.player.stopMove(Vector2(-1, 0), input.keyActionBindings["left"].songTimeLastReleased) #stop moving left
    
    if input.keyActionBindings["right"].justPressed: #if you have tried to move right
        level.player.move(Vector2(1, 0), input.keyActionBindings["right"].songTimeLastPressed) #move right
    elif input.keyActionBindings["right"].justReleased: #if you have stopped trying to move right
        level.player.stopMove(Vector2(1, 0), input.keyActionBindings["right"].songTimeLastReleased) #stop moving right
        
    if input.keyActionBindings["up"].justPressed: #if you have tried to move up
        level.player.move(Vector2(0, -1), input.keyActionBindings["up"].songTimeLastPressed) #move up
    elif input.keyActionBindings["up"].justReleased: #if you have stopped trying to move up
        level.player.stopMove(Vector2(0, -1), input.keyActionBindings["up"].songTimeLastReleased) #stop moving up
        
    if input.keyActionBindings["down"].justPressed: #if you have tried to move down
        level.player.move(Vector2(0, 1), input.keyActionBindings["down"].songTimeLastPressed) #move down
    elif input.keyActionBindings["down"].justReleased: #if you have stopped trying to move down
        level.player.stopMove(Vector2(0, 1), input.keyActionBindings["down"].songTimeLastReleased) #stop moving down

won = False #if you have won
def checkWin(): #check if you have won
    global level, endPositions, endTime, popups, popupOpen, playing, won #globals
    timeSourceTime = songPlayer.getPos() #get the time in the song
    playerState = level.player.calculateState(level, timeSourceTime) #get the player state at that time
    if playerState.pos not in endPositions: #if you are not on an end position
        return #you have not won
    
    if playerState.deathTime is not None and playerState.deathTime <= endTime: #if you died before the end
        return #you have not won

    if playerState.time <= endTime: #if you are not at the end
        return #you have not won
        
    playing = False #you have won, so the level is not playing anymore
    popupOpen = True #a popup is open (the win one)
    won = True #you have won
    songPlayer.pause() #pause the song
    if not popups["win"].open: #if the win popup is not open yet
        popups["win"].texts[-1].text = accText.text #set the accuracy and offset text to the accuracy and offset text (in a somewhat questionable way)
        popups["win"].show() #show the win popup

def update(): #update the game screen
    global playing, popupOpen, popups, playWait #globals
    if playing and not popupOpen: #if the level is playing and no popups are open
        checkInput() #check input
    for popup in popups.values(): #for every popup
        popup.update() #update it
    checkWin() #check if you have won
    if playWait and popups["pause"].closed: #if you're waiting for the popup to close and the popup is closed
        playWait = False #you can stop waiting
        play() #play the level
    
def pause(): #pause the level
    global playing, popups, popupOpen #globals
    songPlayer.pause() #pause the song
    playing = False #the level is not playing
    
    popupOpen = True #a popup is open (the pause one)
    popups["pause"].show() #show the pause popup

def popupClose(): #close all popups
    global popups, popupOpen #globals
    popupOpen = False #no popups are open
    for name, popup in popups.items(): #for every popup
        if popup.open and name != "win": popup.hide() #hide it if it's open and not the win popup (what)

def resume(): #resume the game
    global playWait #globals
    popupClose() #close all popups
    playWait = True #you're waiting for the popup to close

def play(): #play the game
    global playing #globals
    songPlayer.unpause() #unpause the song
    playing = True #the game is playing

def draw(): #draw the game screen
    global accText, endTime, won #globals
    timeSourceTime = songPlayer.getPos() #get the time in the song
    if endTime < timeSourceTime and won: #if the song is over and you have won
        timeSourceTime = endTime #set the time to the end time
    
    playerState = level.player.calculateState(level, timeSourceTime) #get the player state at that time
    if playerState.deathTime is None or playerState.deathTime + level.deathTimeBuffer >= timeSourceTime: #if you are not dead or you are dead but the death time buffer has not passed
        level.draw(gui.screen, timeSourceTime, playerState.visiblePos - Player.offset, level.tileSize, drawPlayer=True, playerState=playerState, freezeTilesOnDeath=True) #draw the level with the player, and freeze tiles on death
    else: #if you are dead and the death time buffer has passed
        level.restart() #restart the level
    
    accText.text = f"Acc: {int(playerState.acc * 1000)}ms\nOffset: {int(playerState.offset * 1000)}ms" #update the accuracy and offset text
    accText.draw() #draw the accuracy and offset text
    
    for popup in popups.values(): #for every popup
        popup.draw() #draw it
        
accText = Text("", 640, 75, (255, 255, 255), 30) #the accuracy and offset text
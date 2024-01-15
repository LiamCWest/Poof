# external imports
import pygame #import the pygame module

# internal imports
from ui.button import Button #import the button class
from utils.polygon import Polygon #import the polygon class
from utils.vector2 import Vector2 #import the vector2 class
from input import input #import the input system

class InputBox(Button): #create a class for buttons that can take keyboard input - inherits from button as they are very similar
    def __init__(self, text, x, y, width, height, color, textColor, textSize = 40, sizeLocked = False, maxLength = 20, scaler = 1.25, clearOnInput = True, numOnly = False, hColor = None, textFont = "ROG"): #initialize the input box
        Button.__init__(self, text, x, y, width, height, color, textColor, self.select, textSize=textSize, scaler=scaler, hColor=hColor, textFont=textFont) #initialize the super class
        self.defaultText = text #set the default text to be displayed before input
        self.clearOnInput = clearOnInput #decide whether to clear the text on input
        self.active = False #set whether or not the box is active
        self.textColor = textColor #set the color of the text
        self.highlightRect = Polygon.fromRect((self.x, self.y, self.width, self.height), self.textColor) #set the highlight rectangle that will appear when the text is highlighted
        self.clicked = False #set whether or not the box is clicked (false on initialization)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) #create the rectangle that contains the input section
        self.output = "" if self.clearOnInput else self.text.text #set the output variable to empty if the text clears on input
        self.returned = False #set if the text has returned
        self.numOnly = numOnly #toggle the restriction of only numerical characters
        self.editable = True #set whether or not the text is editable
        
    def accept(self): #accepts an input from the box and clears the text
        self.returned = False #set the returned bool to False
        if self.clearOnInput: #if the box clears on input
            self.text.text = self.defaultText #set the text to the default text
            self.output = "" #set the output string to an empty string
        
    def deselect(self): #deselects the text box
        if self.active: #if the box is active
            if self.clicked and self.text.text == "": #if the text is empty
                self.clicked = False #toggle clicked off
                self.text.text = self.defaultText #set the text to the default text
            self.active = False #disable active selection
        
    def select(self): #selects the box
        if not self.active and (not self.returned or not self.clearOnInput) and self.editable: #if the box is ready to edit
            if not self.clicked: #if the box has not been clicked yet
                self.text.text = "" #set the text of the box to empty
                self.clicked = True #enable clicked
            self.active = True #enable active selection
        
    def changeText(self, text): #Changes the text on the box
        self.text.text = text #update the text on the box
        self.defaultText = self.text.text #set the default text to the updated text
        self.output = self.text.text #set the output to the text
        
    def update(self, pos = Vector2(0, 0)): #Update the input box
        Button.update(self, pos) #update the super button
        if self.active: #if the input box is active
            if not self.editable: #if the input box is not editable
                self.deselect() #deselect the input box
                return #return 
            for key, value in input.characterBindings.items(): #for the key pressed and its corresponding value in the keybindings
                if value.justPressed: #if the value of a key was just pressed
                    if not self.numOnly or (key.isdigit() or key == "."): self.text.text += key  #constrain the key to a number if numOnly, then add the key to the text
                    
            if input.specialKeyBindings["backspace"].justPressed: #if backspace is pressed
                self.text.text = self.text.text[:-1] #subtract a character
                
            if input.specialKeyBindings["escape"].justPressed: #if escape is pressed
                self.active = False #deselect the select box
                
            if input.specialKeyBindings["enter"].justPressed: #if enter is pressed
                self.output = self.text.text #set the output to the text
                self.returned = True #return the text
                self.active = False #deselect the select box
                
            if input.mouseBindings["lmb"].justPressed: #if mouse is pressed
                if not self.rect.collidepoint(pygame.mouse.get_pos()): #if the mouse is not colliding with the box
                    self.deselect() #deselect the input box
        
    def draw(self, win, pos = Vector2(0, 0)): #draws the box
        Button.draw(self, win, pos) #draw the super button
        if self.active: #if the button is active
            self.highlightRect.scale = self.scale #set the scale of the highlight rect
            self.highlightRect.draw(win, 2, pos = pos) #draw the highlighted rectangle
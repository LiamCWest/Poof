#a class for a button

# external imports
import pygame #import pygame

# internal imports
import input.input as input #import the input system
from utils.vector2 import Vector2 #import the vector2 class
from utils.polygon import Polygon #import the polygon class
from ui.text import Text #import the text class

class Button: #create a class for buttons
    def __init__(self, text, x, y, width, height, color, textColor, onClick = lambda: None, onRelease = lambda: None,z = 0, particles = False, textSize = 40, scaler = 1.25, hColor = None, particlesOnOver = False, textFont = "ROG"): #initializes the button
        self.text = Text(text, x + width//2, y+height//2, textColor, textSize, font = textFont) #create the text object that will be displayed on the button
        self.x = x #set the x position
        self.y = y #set the y position
        self.width = width #set the width of the button
        self.particlesOnOver = particlesOnOver #toggle whether or not particles should exclusively appear when the button is hovered over
        self.height = height #set the height of the button
        self.baseColor = color #set the base color of the button
        self.color = color #set the color of the button (if it needed to be changed later, which it currently doesn't)
        self.scale = 1 #set the scale of the button
        self.scaler = scaler #set the ratio by which the scale changes on hover
        self.emitter = None #set the emitter of the button to none (will be created later if needed)
        self.z = z #set the z position (not used)
        self.particles = particles #set the particle emitter to be used by the button
        self.held = False #set if the button is held down 
        self.onRelease = onRelease #set the command to be executed when the button is released
        self.hColor = hColor if hColor else color #set the color of the highlight to hColor if it exists
        
        if self.particles: #set the particle emitter if it exists
            self.emitter = self.particles #set the particle emitter
            
            w = self.width*(self.scaler-1) #set a var to the width of the button multiplied by the scaler
            h = self.height*(self.scaler-1) #set a var to the heihgt of the button multiplied by the scaler
            
            if self.particlesOnOver: #if the emiiter only creates particles on hover
                self.emitter.shape = Polygon.fromRect((0 - w/2, 0 - h/2, self.width + w, self.height + h), (255, 255, 255)) #set the shape of the emitter to the scaled shape
                #self.emitter = ToggleableShapedEmitter(shape, Vector2(self.x, self.y), Vector2(4,4), 250, 25, 10, H_or_V = "V")
            else: #if the emitter creates particles constantly
                self.emitter.shape = Polygon.fromRect((0, 0, self.width, self.height), (255, 255, 255)) #set the shape of the emitter to the regular shape
                #self.emitter = ShapedEmitter(shape, Vector2(self.x, self.y), Vector2(2,2), 100, 25, 10)
            
            self.emitter.pos = Vector2(self.x, self.y) #set the position of the emitter
        
        self.onClick = onClick #set the function to be called when the button is clicked

    def draw(self, screen, pos = Vector2(0, 0)): #draw the button, its text, and particles
        x = self.x - (self.width * (self.scale - 1) / 2) + pos.x #set the x position
        y = self.y - (self.height * (self.scale - 1) / 2) + pos.y #set the y position
        width = self.width * self.scale #set the width of the shape
        height = self.height * self.scale #set the height of the shape
        if self.particles: #if the button has particles
            self.emitter.draw(screen, pos) #draw the emitter (which draws all the particles)
        rect = pygame.draw.rect(screen, self.color, (x, y, width, height)) #draw a rectangle for the button
        self.text.scale = self.scale #set the scale of the text
        self.text.draw(rect, pos) #draw the text
        
    def isOver(self, pos, pos2): #check if the button is being hovered over
        if pos is None: #if the button doens't have a position
            return False #return false
        return pos2.x < pos.x < (pos2.x + self.width) and pos2.y < pos.y < pos2.y + self.height #return whether or not the mouse coords fall within the bounds of the button
    
    def update(self, pos = Vector2(0, 0)): #update the particles of the button
        if self.particles: #if the button has partilces
            self.emitter.update() #update the emitter (which updates the particles)

        canColorChange = True if self.color in [self.baseColor, self.hColor] else False #check if the button has an available color to change to
        if self.isOver(input.mousePos.pos, Vector2(self.x, self.y) + pos): #if the button is currently hovered over
            if self.particlesOnOver: #if the button has particles when it is hovered over
                self.emitter.go = True #toggle the emitter
            if self.emitter: #if the shape has an emitter
                w = self.width*(self.scaler-1) #set the width of the emitter to be scaled
                h = self.height*(self.scaler-1) #set the height of the emitter to be scaled
                self.emitter.shape = Polygon.fromRect((0 - w/2, 0 - h/2, self.width + w, self.height + h), (255, 255, 255)) #update the emitter shape
            self.scale = self.scaler #update the scale to the scaler
            if canColorChange: self.color = self.hColor #if the color can change, set it to the new color
            if input.mouseBindings["lmb"].justPressed: #if the mouse button is pressed
                self.held = True #toggle the held variable
                self.onClick() #trigger the onclick event
        else: #if the button is not currently hovered over
            if self.particlesOnOver: #if the button has particles exclusively when hovered over
                self.emitter.go = False #toggle the emitter off
            self.scale = 1 #scale the button to normal size
            if self.emitter: #if the button has an emitter
                self.emitter.shape = Polygon.fromRect((0, 0, self.width, self.height), (255, 255, 255)) #set the emitter's shape to the default button size
            if canColorChange: self.color = self.baseColor #if the color can change, revert it to normal
                
        if self.held and not input.mouseBindings["lmb"].pressed: #if the button thinks it's held but is not pressed
            self.held = False #set held to False
            self.onRelease() #trigger the on release event
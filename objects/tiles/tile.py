from objects.gameObject import GameObject
from utils.vector2 import Vector2
from graphics.animation import Animation, AnimEvent, easeOutPow
import input.input as input

class Tile(GameObject):
    def __init__(self, board, pos, size, color, imageName = None):
        self.board = board
        self.relPos = pos
        self.width = size
        self.height = size
        self.updatePos()
        GameObject.__init__(self, self.pos, size, size, color, imageName)
        
    def updatePos(self):
        if hasattr(self, "image") and self.image:
            x = self.relPos.x * self.board.tileSize + round(self.board.tileSize*self.relPos.x*0.1) + self.board.pos.x + (self.board.tileSize//2 - self.imageScale.x*self.image.get_width()//2)
            y = self.relPos.y * self.board.tileSize + round(self.board.tileSize*self.relPos.y*0.1) + self.board.pos.y + (self.board.tileSize//2 - self.imageScale.y*self.image.get_height()//2)
        else:
            x = self.relPos.x * self.board.tileSize + round(self.board.tileSize*self.relPos.x*0.1) + self.board.pos.x + (self.board.tileSize//2 - self.width//2)
            y = self.relPos.y * self.board.tileSize + round(self.board.tileSize*self.relPos.y*0.1) + self.board.pos.y + (self.board.tileSize//2 - self.height//2)
        self.pos = Vector2(x,y)
        
    def appear(self, duration):
        def appearAnim(currentTime):
            self.size = easeOutPow(0, self.board.tileSize, 0, duration, 2, currentTime)
            self.width = self.size
            self.height = self.size
            if self.image:
                self.imageScale = Vector2(self.size/self.image.get_width(), self.size/self.image.get_height())
            self.updatePos()
        
        animEvent = AnimEvent(0, duration, appearAnim)
        anim = Animation([animEvent], input.getRealTime(), "oneShot", duration)
        self.board.addAnimation(anim)

    def disappear(self, duration):
        def disappearAnim(currentTime):
            self.size = easeOutPow(self.board.tileSize, 0, 0, duration, 2, currentTime)
            self.width = self.size
            self.height = self.size
            if self.image:
                self.imageScale = Vector2(self.size/self.image.get_width(), self.size/self.image.get_height())
            # print(self.imageScale.x, self.imageScale.y)
            self.updatePos()
            
        animEvent = AnimEvent(0, duration, disappearAnim)
        anim = Animation([animEvent], input.getRealTime(), "oneShot", duration)
        self.board.addAnimation(anim)
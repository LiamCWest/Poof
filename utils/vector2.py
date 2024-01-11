import math

class Vector2:
    def __init__(self, x ,y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, other):
        return Vector2(self.x * other.x, self.y * other.y)
    
    def __truediv__(self, other):
        return Vector2(self.x / other.x, self.y / other.y)
    
    def __floordiv__(self, other):
        return Vector2(self.x // other.x, self.y // other.y)
    
    def __mod__(self, other):
        return Vector2(self.x % other.x, self.y % other.y)
    
    def __pow__(self, other):
        return Vector2(self.x ** other.x, self.y ** other.y)
    
    def __neg__(self):
        return Vector2(-self.x, -self.y)
    
    def __pos__(self):
        return Vector2(+self.x, +self.y)
    
    def __abs__(self):
        return Vector2(abs(self.x), abs(self.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
    
    def __str__(self):
        return f"Vector2({self.x}, {self.y})"
    
    def __hash__(self):
        return hash(self.toTuple())
    
    def copy(self):
        return Vector2(self.x, self.y)
    
    def multiply(self, other):
        return Vector2(self.x * other, self.y * other)
    
    def divide(self, other):
        return Vector2(self.x / other, self.y / other)
    
    def add(self, other):
        return Vector2(self.x + other, self.y + other)
    
    def sub(self, other):
        return Vector2(self.x - other, self.y - other)
    
    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector2(0, 0)
        else:
            return self.divide(length)

    def length(self):
        return math.sqrt(math.pow(self.x,2) + math.pow(self.y,2))
    
    def toTuple(self):
        return (self.x, self.y)
    
    def invert(self):
        return Vector2(-self.x, -self.y)
    
    def round(self):
        return Vector2(round(self.x), round(self.y))
    
    def floor(self):
        return Vector2(math.floor(self.x), math.floor(self.y))
    
    def distance(self, other):
        return (self - other).length()
    
    @classmethod
    def from_tuple(cls, tuple):
        return cls(*tuple)

UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
RIGHT = Vector2(1, 0)
LEFT = Vector2(-1, 0)
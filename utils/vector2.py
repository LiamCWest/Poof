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
        return Vector2(self.x == other.x, self.y == other.y)
    
    def __ne__(self, other):
        return Vector2(self.x != other.x, self.y != other.y)
    
    def __lt__(self, other):
        return Vector2(self.x < other.x, self.y < other.y)
    
    def __le__(self, other):
        return Vector2(self.x <= other.x, self.y <= other.y)
    
    def __gt__(self, other):
        return Vector2(self.x > other.x, self.y > other.y)
    
    def __ge__(self, other):
        return Vector2(self.x >= other.x, self.y >= other.y)
    
    def copy(self):
        return Vector2(self.x, self.y)
    
    def multiply(self, other):
        return Vector2(self.x * other, self.y * other)

UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
RIGHT = Vector2(1, 0)
LEFT = Vector2(-1, 0)
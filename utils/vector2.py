#a vector2, can represent a position or a direction or other things

# external imports
import math # for math functions

class Vector2: # a class representing a vector2
    def __init__(self, x ,y): # constructor
        self.x = x # set the x value
        self.y = y # set the y value
    
    def __add__(self, other): # called when adding two vectors
        return Vector2(self.x + other.x, self.y + other.y) # return the sum of the two vectors
    
    def __sub__(self, other): # called when subtracting two vectors
        return Vector2(self.x - other.x, self.y - other.y) # return the difference of the two vectors
    
    def __mul__(self, other): # called when multiplying two vectors
        return Vector2(self.x * other.x, self.y * other.y) # return the product of the two vectors (not a real vector operation but useful)
    
    def __truediv__(self, other): # called when dividing two vectors
        return Vector2(self.x / other.x, self.y / other.y) # return the quotient of the two vectors (not a real vector operation but useful)
    
    def __floordiv__(self, other): # called when floor dividing two vectors
        return Vector2(self.x // other.x, self.y // other.y) # return the floor quotient of the two vectors (not a real vector operation but occasionally useful)
    
    def __mod__(self, other): # called when modding two vectors
        return Vector2(self.x % other.x, self.y % other.y) # return the mod of the two vectors (not a real vector operation but occasionally useful)
    
    def __pow__(self, other): # called when exponentiating two vectors
        return Vector2(self.x ** other.x, self.y ** other.y) # return the exponent of the two vectors (not a real vector operation but occasionally useful)
    
    def __neg__(self): # called when negating a vector
        return Vector2(-self.x, -self.y) # return the negation of the vector
    
    def __pos__(self): # called when positing a vector
        return Vector2(self.x, self.y) # return the positing of the vector (what is the point of this?)
    
    def __abs__(self): # called when getting the absolute value of a vector
        return Vector2(abs(self.x), abs(self.y)) # return the absolute value of the vector (not a real vector operation but occasionally useful)
    
    def __eq__(self, other): # called when checking if two vectors are equal
        return self.x == other.x and self.y == other.y # return if the two vectors are equal
    
    def __ne__(self, other): # called when checking if two vectors are not equal
        return self.x != other.x or self.y != other.y # return if the two vectors are not equal
    
    def __str__(self): # called when converting a vector to a string
        return f"Vector2({self.x}, {self.y})" # return the vector as a string
    
    def __hash__(self): # called when hashing a vector
        return hash(self.toTuple()) # return the hash of the vector
    
    def copy(self): # returns a copy of the vector
        return Vector2(self.x, self.y) # return a copy of the vector
    
    def multiply(self, other): # multiplies the vector by a scalar
        return Vector2(self.x * other, self.y * other) # return the product of the vector and the scalar
    
    def divide(self, other): # divides the vector by a scalar
        return Vector2(self.x / other, self.y / other) # return the quotient of the vector and the scalar
    
    def add(self, other): # adds a scalar to the vector
        return Vector2(self.x + other, self.y + other) # return the sum of the vector and the scalar (not a real vector operation but occasionally useful)
    
    def sub(self, other): # subtracts a scalar from the vector
        return Vector2(self.x - other, self.y - other) # return the difference of the vector and the scalar (not a real vector operation but occasionally useful)
    
    def normalize(self): # normalizes the vector
        length = self.length() # get the length of the vector
        if length == 0: # if the length is 0
            return Vector2(0, 0) # return the 0 vector
        else: # if the length is not 0
            return self.divide(length) # return the vector divided by its length

    def length(self): # returns the length of the vector
        return math.sqrt(math.pow(self.x,2) + math.pow(self.y,2)) # return the length of the vector
    
    def toTuple(self): # returns the vector as a tuple
        return (self.x, self.y) # return the vector as a tuple
    
    def round(self): # rounds the vector
        return Vector2(round(self.x), round(self.y)) # return the vector rounded
    
    def floor(self): # floors the vector
        return Vector2(math.floor(self.x), math.floor(self.y)) # return the vector floored
    
    def distance(self, other): # returns the distance between two vectors (only makes sense if considering them as points really)
        return (self - other).length() # return the length of the difference of the two vectors
    
    @classmethod # a class method
    def from_tuple(cls, tuple): # creates a vector from a tuple
        return cls(*tuple) # return a vector from the tuple

UP = Vector2(0, -1) #the vector that points up
DOWN = Vector2(0, 1) #the vector that points down
RIGHT = Vector2(1, 0) #the vector that points right
LEFT = Vector2(-1, 0) #the vector that points left
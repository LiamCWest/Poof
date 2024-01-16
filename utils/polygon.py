#a polygon, used many times in the game

# external imports
import random # for random numbers
import pygame # for drawing to the screen

# internal imports
from utils.vector2 import Vector2 # for vector operations

class Polygon: # a class representing a polygon
    def __init__(self, points, color = (0,0,0)): # constructor
        self.pos = Vector2(0,0) # the position of the polygon
        self.points = points # the vertices of the polygon
        self.color = color # the color of the polygon
        self.calc() # calculate the edges and normals of the polygon
        self.scale = 1 # the scale of the polygon

    def calc(self): # calculates the edges and normals of the polygon
        self.edges = [] # the edges of the polygon are an empty list to start
        self.normals = [] # the normals of the polygon are an empty list to start
        self.calcEdges() # calculate the edges of the polygon
        self.calcNormals() # calculate the normals of the polygon
        
    def calcEdges(self): # calculates the edges of the polygon
        for i in range(len(self.points)): # for each point in the polygon
            self.edges.append(Edge(Vector2.from_tuple(self.points[i]), Vector2.from_tuple(self.points[(i + 1) % len(self.points)]))) # add the edge from the current point to the next point to the edges list
            
    def calcNormals(self): # calculates the normals of the edges of the polygon
        for edge in self.edges: # for each edge in the polygon
            self.normals.append(edge.normal()) # add the normal of the edge to the normals list

    def draw(self, screen, outlineWidth = 0, outlineColor = None, pos = Vector2(0,0)): # draws the polygon to the screen
        points = [] # the points of the polygon to draw
        for i in range(len(self.points)): # for each point in the polygon
            point = Vector2.from_tuple(self.points[i]) # get the point
            point = point.multiply(self.scale) # scale the point
            point += self.pos + pos # add the position of the polygon to the point
            points.append(point.toTuple()) # add the point to the points list
        if outlineWidth != 0: # if the polygon has an outline
            color = outlineColor if outlineColor else self.color # if the polygon has an outline color, use that, otherwise use the polygon's color
            pygame.draw.polygon(screen, color, points, outlineWidth) # draw the polygon with an outline
        else: # if the polygon does not have an outline
            pygame.draw.polygon(screen, self.color, points) # draw the polygon without an outline
    
    def move(self, delta): # moves the polygon by a vector
        self.pos += delta # add the vector to the position of the polygon
    
    def weightedRandomEdge(self, edges):
        weights = [edge.p1.distance(edge.p2) for edge in edges] #weights are the length of the edges
        return random.choices(edges, weights)[0] #randomly choose an edge based on the weights
    
    def randomPointOnEdge(self): #random position along edge of polygon
        edge = self.weightedRandomEdge(self.edges) #random edge
        scalar = random.uniform(0,1) #random scalar
        randomPoint = edge.p1 + (edge.p2 - edge.p1).multiply(scalar) #random point on edge
        return randomPoint+self.pos #return random point on edge
    
    def randomPointOnParallelRectangleSides(self, H_or_V = "H"): #random position on parallel sides of rectangle        
        if H_or_V == "H": #horizontal
            edge = self.weightedRandomEdge([self.edges[0],self.edges[2]]) #random horizontal edge
        else: #vertical
            edge = self.weightedRandomEdge([self.edges[1],self.edges[3]]) #random vertical edge
        
        scalar = random.uniform(0,1) #random scalar
        randomPoint = edge.p1 + (edge.p2 - edge.p1).multiply(scalar) #random point on edge
        return randomPoint+self.pos #return random point on edge
            
    def dirAt(self, pos): #angle from pos to center of polygon as a vector2 (normalized)
        return (pos-self.pos).normalize() #return normalized vector from pos to center of polygon

    def getWidth(self): #width of polygon
        return max(self.points, key=lambda x: x[0])[0] - min(self.points, key=lambda x: x[0])[0] #return max x - min x
    
    def getHeight(self): #height of polygon
        return max(self.points, key=lambda x: x[1])[1] - min(self.points, key=lambda x: x[1])[1] #return max y - min y
    
    @classmethod # a class method
    def fromRect(cls, rect, color = (0,0,0)): # creates a polygon from a rectangle
        #create polygon from rect 
        poly = cls([(rect[2]//2*-1, rect[3]//2*-1), #top left
                    (rect[2]//2, rect[3]//2*-1), #top right
                    (rect[2]//2, rect[3]//2), #bottom right
                    (rect[2]//2*-1, rect[3]//2)], color) #bottom left and color
        poly.pos = Vector2(rect[0] + rect[2]//2, rect[1] + rect[3]//2) #set position of polygon to center of rect
        return poly #return polygon
        
class Edge: # a class representing an edge of a polygon
    def __init__(self, p1, p2): # constructor
        self.p1 = p1 # the first point of the edge 
        self.p2 = p2 # the second point of the edge
        
    def normal(self): # returns the normal of the edge
        return Vector2(-(self.p2.y - self.p1.y), self.p2.x - self.p1.x).normalize() # return the normal of the edge
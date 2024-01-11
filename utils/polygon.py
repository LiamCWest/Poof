from utils.vector2 import Vector2
import random
import pygame

class Polygon:
    def __init__(self, points, color = (0,0,0)):
        self.pos = Vector2(0,0)
        self.points = points
        self.color = color
        self.calc()
        self.scale = 1

    def calc(self):
        self.edges = []
        self.normals = []
        self.calcEdges()
        self.calcNormals()

    def draw(self, screen, outlineWidth = 0, outlineColor = None, pos = Vector2(0,0)):
        points = []
        for i in range(len(self.points)):
            point = Vector2.from_tuple(self.points[i])
            # scale
            point = point.multiply(self.scale)
            # translate
            point += self.pos + pos
            points.append(point.toTuple())
        if outlineWidth != 0:
            color = outlineColor if outlineColor else self.color
            pygame.draw.polygon(screen, color, points, outlineWidth)
        else:
            pygame.draw.polygon(screen, self.color, points)
    
    def move(self, delta):
        self.pos += delta
        
    def calcEdges(self):
        for i in range(len(self.points)):
            self.edges.append(Edge(Vector2.from_tuple(self.points[i]), Vector2.from_tuple(self.points[(i + 1) % len(self.points)])))
            
    def calcNormals(self):
        for edge in self.edges:
            self.normals.append(edge.normal())
    
    def weightedRandomEdge(self, edges):
        #random edge of polygon, weighted by length
        weights = [edge.p1.distance(edge.p2) for edge in edges]
        return random.choices(edges, weights)[0]
    
    def randomPointOnEdge(self):
        #random position along edge of polygon
        edge = self.weightedRandomEdge(self.edges)
        x = random.uniform(edge.p1.x, edge.p2.x)
        y = random.uniform(edge.p1.y, edge.p2.y)
        return Vector2(x,y)+self.pos
    
    def randomPointOnParallelRectangleSides(self, H_or_V = "H"):
        if len(self.edges) != 4:
            print("Don't use this function on non-quadrilateral shapes")
        
        if H_or_V == "H":
            edge = self.weightedRandomEdge([self.edges[0],self.edges[2]])
        else:
            edge = self.weightedRandomEdge([self.edges[1],self.edges[3]])
        
        x = random.uniform(edge.p1.x, edge.p2.x)
        y = random.uniform(edge.p1.y, edge.p2.y)
        return Vector2(x,y)+self.pos
            
    def dirAt(self, pos):
        #angle from pos to center of polygon as a vector2 (normalized)
        return (pos-self.pos).normalize()

    def getWidth(self):
        #width of polygon
        return max(self.points, key=lambda x: x[0])[0] - min(self.points, key=lambda x: x[0])[0]
    
    def getHeight(self):
        #height of polygon
        return max(self.points, key=lambda x: x[1])[1] - min(self.points, key=lambda x: x[1])[1]
    
    @classmethod
    def fromRect(cls, rect, color = (0,0,0)):
        #create polygon from rect 
        poly = cls([(rect[2]//2*-1, rect[3]//2*-1), 
                    (rect[2]//2, rect[3]//2*-1), 
                    (rect[2]//2, rect[3]//2), 
                    (rect[2]//2*-1, rect[3]//2)], color)
        poly.pos = Vector2(rect[0] + rect[2]//2, rect[1] + rect[3]//2)
        return poly     
        
class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
    def normal(self):
        return Vector2(-(self.p2.y - self.p1.y), self.p2.x - self.p1.x).normalize()
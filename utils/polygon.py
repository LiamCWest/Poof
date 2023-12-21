from utils.vector2 import Vector2
import random

class Polygon:
    def __init__(self, points):
        self.points = points
        self.edges = []
        self.normals = []
        self.calcEdges()
        self.calcNormals()
        
    def calcEdges(self):
        for i in range(len(self.points)):
            self.edges.append(Edge(Vector2.from_tuple(self.points[i]), Vector2.from_tuple(self.points[(i + 1) % len(self.points)])))
            
    def calcNormals(self):
        for edge in self.edges:
            self.normals.append(edge.normal())
            
    def randomPointOnEdge(self):
        #random position along edge of polygon
        edge = random.choice(self.edges)
        return Vector2(random.uniform(edge.p1.x, edge.p2.x), random.uniform(edge.p1.y, edge.p2.y))
            
    def dirAt(self, pos):
        #angle from pos to center of polygon as a vector2 (normalized)
        return (self.center() - pos).normalize().invert()
    
    def center(self):
        #center of polygon
        x = 0
        y = 0
        for point in self.points:
            x += point[0]
            y += point[1]
        return Vector2(x / len(self.points), y / len(self.points))
        
        
class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
    def normal(self):
        return Vector2(-(self.p2.y - self.p1.y), self.p2.x - self.p1.x).normalize()
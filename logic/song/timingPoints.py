from utils.binarySearch import binarySearch

class timeSignature:
    def __init__(self, num, denom):
        self.num = num
        self.denom = denom

class timingPoint:
    def __init__(self, time, bpm, timeSignature):
        self.time = time
        self.bpm = bpm
        self.timeSignature = timeSignature

def getPreviousPoint(points, time):
    index = binarySearch(points, time, lambda time, point: time - point.time)
    if index == -1:
        return None
    return points[index]

def getNextPoint(points, time):
    index = binarySearch(points, time, lambda time, point: time - point.time)
    if index == len(points) - 1:
        return None
    return points[index + 1]


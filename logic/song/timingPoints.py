from utils.binarySearch import binarySearch
import math

class timeSignature:
    def __init__(self, num, denom):
        self.num = num
        self.denom = denom

class timingPoint:
    def __init__(self, time, bpm, timeSignature):
        self.time = time
        self.bpm = bpm
        self.beatLength = 60 / bpm
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

def getPreviousBeat(points, time, divisor):
    point = getPreviousPoint(points, time)
    if point == None:
        return None
    timeSinceLastPoint = time - point.time
    beatsElapsed = timeSinceLastPoint * divisor / point.beatLength
    return math.floor(beatsElapsed) * point.beatLength / divisor + point.time

def getNextBeat(points, time, divisor):
    point = getPreviousPoint(points, time)
    if point == None:
        return None
    timeSinceLastPoint = time - point.time
    beatsElapsed = timeSinceLastPoint * divisor / point.beatLength
    return math.floor(beatsElapsed + 1) * point.beatLength / divisor + point.time

def test():
    timingPoint1 = timingPoint(0, 120, timeSignature(4, 4))
    timingPoint2 = timingPoint(6, 130, timeSignature(7, 2))
    timingPoints = [timingPoint1, timingPoint2]
    beat = getNextBeat(timingPoints, 6.1, 1)
    print(beat)
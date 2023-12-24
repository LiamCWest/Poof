from utils.binarySearch import binarySearch
import math

class TimeSignature:
    def __init__(self, num, denom):
        self.num = num
        self.denom = denom

class TimingPoint:
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
    if len(points) == 0:
        return None
    
    point = getPreviousPoint(points, time)
    if point == None:
        point = points[0]
        timeUntilFirstPoint = point.time - time
        beatsWillBeElapsed = timeUntilFirstPoint * divisor / point.beatLength
        return point.time - (math.ceil(beatsWillBeElapsed) * point.beatLength / divisor)
    timeSinceLastPoint = time - point.time
    beatsElapsed = timeSinceLastPoint * divisor / point.beatLength
    return math.floor(beatsElapsed) * point.beatLength / divisor + point.time

def getNextBeat(points, time, divisor): #TODO: Make sure none of these getBeat functions have subtle errors
    if len(points) == 0:
        return None
    
    point = getPreviousPoint(points, time)
    if point == None:
        point = points[0]
        timeUntilFirstPoint = point.time - time
        beatsWillBeElapsed = timeUntilFirstPoint * divisor / point.beatLength
        return point.time - (math.floor(beatsWillBeElapsed) * point.beatLength / divisor)
    timeSinceLastPoint = time - point.time
    beatsElapsed = timeSinceLastPoint * divisor / point.beatLength
    return math.ceil(beatsElapsed) * point.beatLength / divisor + point.time

def getBeatByIndex(points, index, divisor):
    if len(points) == 0:
        return None
    
    beatsRemaining = index
    for i in range(len(points) - 1):
        timeInPoint = points[i + 1].time - points[i].time
        beatsInPoint = math.floor(timeInPoint * divisor / points[i].beatLength)
        beatsRemaining -= beatsInPoint
        
        if beatsRemaining < 0:
            beatsRemaining += beatsInPoint
            return points[i].time + math.floor(beatsRemaining * points[i].beatLength / divisor)
    return points[len(points) - 1].time + beatsRemaining * points[len(points) - 1].beatLength / divisor

def test():
    timingPoint1 = TimingPoint(0, 120, TimeSignature(4, 4))
    timingPoint2 = TimingPoint(6, 130, TimeSignature(7, 2))
    timingPoints = [timingPoint1, timingPoint2]
    beat = getNextBeat(timingPoints, 6.1, 1)
    print(beat)
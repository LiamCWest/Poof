from ...utils.binarySearch import binarySearch
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
    timeSinceLastPoint = time - point.time
    beatsElapsed = timeSinceLastPoint * divisor / point.beatLength
    return math.floor(beatsElapsed) * point.beatLength + point.time

def getNextBeat(points, time, divisor):
    point = getPreviousPoint(points, time)
    timeSinceLastPoint = time - point.time
    beatsElapsed = timeSinceLastPoint * divisor / point.beatLength
    return math.floor(beatsElapsed + 1) * point.beatLength + point.time

if __name__ == "__main__":
    timingPoint1 = timingPoint(0, 120, timeSignature(4, 4))
    timingPoint2 = timingPoint(6, 130, timeSignature(7, 2))
    timingPoints = [timingPoint1, timingPoint2]
    for i in range(10):
        print(getPreviousPoint(timingPoints, i / 2), getNextPoint(timingPoints, i / 2))
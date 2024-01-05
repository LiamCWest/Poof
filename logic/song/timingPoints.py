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
        
    def toValues(self):
        return [self.time, self.bpm, self.timeSignature.num, self.timeSignature.denom]

def getPreviousPointIndex(points, time):
    return binarySearch(points, time, lambda time, point: time - point.time)

def getPreviousPoint(points, time):
    index = getPreviousPointIndex(points, time)
    if index == -1:
        return None
    return points[index]

def getNextPoint(points, time):
    index = getPreviousPointIndex(points, time)
    if index == len(points) - 1:
        return None
    return points[index + 1]

def isOnBeat(time, point, divisor, pointIsAfter = False): #haha yes i can remove the need for epsilon now
    if pointIsAfter:
        timeUntilPoint = point.time - time
        dividedBeatLength = point.beatLength / divisor
        beatsUntil = timeUntilPoint / dividedBeatLength
        roundedBeatsUntil = round(beatsUntil)
        
        timeOfNearestBeat = -roundedBeatsUntil * dividedBeatLength + point.time
        return timeOfNearestBeat == time
    
    timeSincePoint = time - point.time
    dividedBeatLength = point.beatLength / divisor
    beatsElapsed = timeSincePoint / dividedBeatLength
    roundedBeatsElapsed = round(beatsElapsed)
    
    timeOfNearestBeat = roundedBeatsElapsed * dividedBeatLength + point.time
    return timeOfNearestBeat == time

def getPreviousBeat(points, time, divisor):
    if len(points) == 0:
        return None
    
    pointIndex = getPreviousPointIndex(points, time)
    if pointIndex == -1: #if you're before the first point
        point = points[0]
        timeUntilPoint = point.time - time
        dividedBeatLength = point.beatLength / divisor
        beatsUntil = timeUntilPoint / dividedBeatLength
        if isOnBeat(time, point, divisor, True): #if you're on a beat
            realBeatsUntil = round(beatsUntil) + 1
            timeOfPreviousBeat = -realBeatsUntil * dividedBeatLength + point.time
        else:
            ceiledBeatsUntil = math.ceil(beatsUntil)
            timeOfPreviousBeat = -ceiledBeatsUntil * dividedBeatLength + point.time
        return timeOfPreviousBeat
        
    point = points[pointIndex]
    
    timeSincePoint = time - point.time
    dividedBeatLength = point.beatLength / divisor
    beatsElapsed = timeSincePoint / dividedBeatLength
    if not isOnBeat(time, point, divisor): #if you're not on a beat
        flooredBeatsElapsed = math.floor(beatsElapsed)
        timeOfPreviousBeat = flooredBeatsElapsed * dividedBeatLength + point.time
        return timeOfPreviousBeat
    
    roundedBeatsElapsed = round(beatsElapsed)
    if roundedBeatsElapsed != 0: #if you're not on a timing point
        timeOfPreviousBeat = (roundedBeatsElapsed - 1) * dividedBeatLength + point.time
        return timeOfPreviousBeat
            
    newPointIndex = pointIndex
    while newPointIndex > 0: #if you're not on the first timing point
        newPointIndex -= 1
        lastPoint = points[newPointIndex]
        
        if lastPoint.time == point.time: #ignore duplicate timing points
            continue
        
        dividedBeatLength = lastPoint.beatLength / divisor
        lastPointDuration = point.time - lastPoint.time
        beatsInPoint = lastPointDuration / dividedBeatLength
        flooredBeatsInPoint = math.floor(beatsInPoint)
        timeOfPreviousBeat = flooredBeatsInPoint * dividedBeatLength + lastPoint.time
        
        if timeOfPreviousBeat < time: #if the beat found is not the same as the current time
            return timeOfPreviousBeat
        
        #flooredBeatsInPoint should never be 0 here
        timeOfPreviousBeat = (flooredBeatsInPoint - 1) * dividedBeatLength + lastPoint.time
        return timeOfPreviousBeat
        
    return points[0].time - (points[0].beatLength / divisor) #if you are exactly on the first timing point

def getNextBeat(points, time, divisor, countSameBeat = False): #TODO: Make sure none of these getBeat functions have subtle errors
    if len(points) == 0: #if you're before the first point
        return None

    pointIndex = getPreviousPointIndex(points, time)
    if pointIndex == -1: #if you're before the first point
        point = points[0]
        timeUntilPoint = point.time - time
        dividedBeatLength = point.beatLength / divisor
        beatsUntil = timeUntilPoint / dividedBeatLength
        if isOnBeat(time, point, divisor, True): #if you're on a beat
            realBeatsUntil = round(beatsUntil) - 1
            timeOfPreviousBeat = -realBeatsUntil * dividedBeatLength + point.time
        else:
            flooredBeatsUntil = math.floor(beatsUntil)
            timeOfPreviousBeat = -flooredBeatsUntil * dividedBeatLength + point.time
        return timeOfPreviousBeat
    
    point = points[pointIndex]
    
    if point.time == time: #if you're on a point        
        newPointIndex = pointIndex
        nextPoint = points[newPointIndex]
        while newPointIndex < len(points): #find the latest point with the same time
            nextPoint = points[newPointIndex]
            
            if nextPoint.time != time:
                newPointIndex -= 1
                nextPoint = points[newPointIndex]
                break
            
            newPointIndex += 1
        
        dividedBeatLength = nextPoint.beatLength / divisor
        timeOfNextBeat = dividedBeatLength + nextPoint.time
        
        if len(points) > newPointIndex + 1: #if the beat found surpasses the time of the next point
            nextPoint = points[newPointIndex + 1]
            if timeOfNextBeat > nextPoint.time:
                timeOfNextBeat = nextPoint.time
                
        return timeOfNextBeat

    timeSincePoint = time - point.time
    dividedBeatLength = point.beatLength / divisor
    beatsElapsed = timeSincePoint / dividedBeatLength
    if isOnBeat(time, point, divisor): #if you're on a beat
        realBeatsElapsed = round(beatsElapsed) + 1
        timeOfNextBeat = realBeatsElapsed * dividedBeatLength + point.time
    else:
        ceiledBeatsElapsed = math.ceil(beatsElapsed)
        timeOfNextBeat = ceiledBeatsElapsed * dividedBeatLength + point.time
    
    if len(points) > pointIndex + 1:
        nextPoint = points[pointIndex + 1]
        if timeOfNextBeat > nextPoint.time: #if the beat found surpasses the time of the next point
            timeOfNextBeat = nextPoint.time
    
    return timeOfNextBeat

def getNearestBeat(points, time, divisor):
    def getCloserBeat(previous, next, time):
        if abs(previous - time) < abs(next - time):
            return previous
        return next
    
    if len(points) == 0: #if you're before the first point
        return None
    
    pointIndex = getPreviousPointIndex(points, time)
    if pointIndex == -1: #if you're before the first point
        point = points[0]
        timeUntilPoint = point.time - time
        dividedBeatLength = point.beatLength / divisor
        beatsUntil = timeUntilPoint / dividedBeatLength
        if isBeatNumInt(beatsUntil): #if you're on a beat
            return time
        previousBeat = getPreviousBeat(points, time, divisor)
        nextBeat = getNextBeat(points, time, divisor)
        return getCloserBeat(previousBeat, nextBeat, time)
    
    point = points[pointIndex]
    
    timeSincePoint = time - point.time
    dividedBeatLength = point.beatLength / divisor
    beatsElapsed = timeSincePoint / dividedBeatLength
    if isBeatNumInt(beatsElapsed): #if you're on a beat
        return time
    previousBeat = getPreviousBeat(points, time, divisor)
    nextBeat = getNextBeat(points, time, divisor)
    return getCloserBeat(previousBeat, nextBeat, time)

def test():
    timingPoint1 = TimingPoint(0, 120, TimeSignature(4, 4))
    timingPoint2 = TimingPoint(6, 130, TimeSignature(7, 2))
    timingPoints = [timingPoint1, timingPoint2]
    beat = getNextBeat(timingPoints, 6.1, 1)
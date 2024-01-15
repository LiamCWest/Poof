# external imports
import math #math

# internal imports
from utils.binarySearch import binarySearch #for binary searching

class TimeSignature: #a struct for a time signature
    def __init__(self, num, denom): #constructor
        self.num = num #numerator
        self.denom = denom #denominator

class TimingPoint: #a struct for a timing point
    def __init__(self, time, bpm, timeSignature): #constructor
        self.time = time #time in seconds
        self.bpm = bpm #beats per minute
        self.timeSignature = timeSignature #time signature
        
    beatLength = property(lambda self: 60/self.bpm) #length of a beat in seconds, calculated from bpm
        
    def toValues(self): #returns a list of the values of the timing point
        return [self.time, self.bpm, self.timeSignature.num, self.timeSignature.denom] #return the values

def getPreviousPointIndex(points, time): #returns the index of the previous timing point
    return binarySearch(points, time, lambda time, point: time - point.time) #binary search for the previous timing point and return it

def getPreviousPoint(points, time): #returns the previous timing point
    index = getPreviousPointIndex(points, time) #get the index of the previous timing point
    if index == -1: #if there is no previous timing point
        return None #return None
    return points[index] #return the previous timing point

def getNextPoint(points, time): #returns the next timing point
    index = getPreviousPointIndex(points, time) #get the index of the previous timing point
    if index == len(points) - 1: #if there is no next timing point
        return None #return None
    return points[index + 1] #return the next timing point

def isOnBeat(time, point, divisor, pointIsAfter = False): #determines if a inputted time is on a beat. pointIsAfter is if the first timing point is after the input time
    if pointIsAfter: #if the first timing point is after the input time
        timeUntilPoint = point.time - time #time until the first timing point
        dividedBeatLength = point.beatLength / divisor #length of a subdivided beat
        beatsUntil = timeUntilPoint / dividedBeatLength #beats until the first timing point
        roundedBeatsUntil = round(beatsUntil) #rounded beats until the first timing point
        
        timeOfNearestBeat = -roundedBeatsUntil * dividedBeatLength + point.time #recalculate the time of the nearest beat based on the rounded beats until
        return timeOfNearestBeat == time #if the time of the nearest beat is equal to the input time, then the input time is on a beat
    
    timeSincePoint = time - point.time #time since the previous timing point
    dividedBeatLength = point.beatLength / divisor #length of a subdivided beat
    beatsElapsed = timeSincePoint / dividedBeatLength #beats elapsed since the previous timing point
    roundedBeatsElapsed = round(beatsElapsed) #rounded beats elapsed since the previous timing point
    
    timeOfNearestBeat = roundedBeatsElapsed * dividedBeatLength + point.time #recalculate the time of the nearest beat based on the rounded beats elapsed
    return timeOfNearestBeat == time #if the time of the nearest beat is equal to the input time, then the input time is on a beat

def getBeatsSincePoint(time, point, divisor): #returns the number of beats since the previous timing point
    timeSincePoint = time - point.time #time since the previous timing point
    dividedBeatLength = point.beatLength / divisor #length of a subdivided beat
    beatsElapsed = timeSincePoint / dividedBeatLength #beats elapsed since the previous timing point
    roundedBeatsElapsed = round(beatsElapsed) #rounded beats elapsed since the previous timing point
    
    timeOfNearestBeat = roundedBeatsElapsed * dividedBeatLength + point.time #recalculate the time of the nearest beat based on the rounded beats elapsed
    
    if time >= timeOfNearestBeat: #if the input time is after the time of the nearest beat
        return roundedBeatsElapsed #return the rounded beats elapsed
    return roundedBeatsElapsed - 1 #else return the rounded beats elapsed minus 1

def getPreviousBeat(points, time, divisor): #returns the time of the previous beat
    if len(points) == 0: #if there are no timing points
        return None #return None
    
    pointIndex = getPreviousPointIndex(points, time) #get the index of the previous timing point
    if pointIndex == -1: #if you're before the first point
        point = points[0] #get the first point
        timeUntilPoint = point.time - time #get the time until the first point
        dividedBeatLength = point.beatLength / divisor #get the length of a subdivided beat
        beatsUntil = timeUntilPoint / dividedBeatLength #get the beats until the first point
        if isOnBeat(time, point, divisor, True): #if you're on a beat
            realBeatsUntil = round(beatsUntil) + 1 #then beatsUntil would calculate to this time, so add 1
            timeOfPreviousBeat = -realBeatsUntil * dividedBeatLength + point.time #recalculate the time of the previous beat based on the real beats until
        else: #else you're not on a beat
            ceiledBeatsUntil = math.ceil(beatsUntil) #ceil beats until to round up to the previous beat
            timeOfPreviousBeat = -ceiledBeatsUntil * dividedBeatLength + point.time #recalculate the time of the previous beat based on the ceiled beats until
        return timeOfPreviousBeat #return the time of the previous beat
        
    point = points[pointIndex] #else get the previous point
    
    timeSincePoint = time - point.time #time since the previous timing point
    dividedBeatLength = point.beatLength / divisor #length of a subdivided beat
    beatsElapsed = timeSincePoint / dividedBeatLength #beats elapsed since the previous timing point
    if not isOnBeat(time, point, divisor): #if you're not on a beat
        flooredBeatsElapsed = math.floor(beatsElapsed) #floor beats elapsed to round down to the previous beat
        timeOfPreviousBeat = flooredBeatsElapsed * dividedBeatLength + point.time #calculate the time of the previous beat based on the floored beats elapsed
        return timeOfPreviousBeat #return the time of the previous beat
    
    roundedBeatsElapsed = round(beatsElapsed) #else you're on a beat, so get the rounded beats elapsed since the previous timing point
    if roundedBeatsElapsed != 0: #if you're not on a timing point
        timeOfPreviousBeat = (roundedBeatsElapsed - 1) * dividedBeatLength + point.time #calculate the time of the previous beat based on the rounded beats elapsed - 1
        return timeOfPreviousBeat #return the time of the previous beat
            
    newPointIndex = pointIndex #else you're on a timing point, so find the latest point with the same time
    while newPointIndex > 0: #if you're not on the first timing point
        newPointIndex -= 1 #go to the previous timing point
        lastPoint = points[newPointIndex] #get the previous timing point
        
        if lastPoint.time == point.time: #ignore duplicate timing points
            continue #continue until the timing point is at a different time
        
        dividedBeatLength = lastPoint.beatLength / divisor #length of a subdivided beat
        lastPointDuration = point.time - lastPoint.time #duration of the previous timing point
        beatsInPoint = lastPointDuration / dividedBeatLength #beats that occur in the previous timing point
        flooredBeatsInPoint = math.floor(beatsInPoint) #floor beats in point to get an integer
        timeOfPreviousBeat = flooredBeatsInPoint * dividedBeatLength + lastPoint.time #calculate the time of the previous beat based on the floored beats in point
        
        if timeOfPreviousBeat < time: #if the beat found is not the same as the current time
            return timeOfPreviousBeat #return the time of the previous beat
        
        timeOfPreviousBeat = (flooredBeatsInPoint - 1) * dividedBeatLength + lastPoint.time #else calculate the time of the previous beat based on the floored beats in point - 1
        return timeOfPreviousBeat #return the time of the previous beat
        
    return points[0].time - (points[0].beatLength / divisor) #if you are exactly on the first timing point

def getNextBeat(points, time, divisor): #returns the time of the next beat
    if len(points) == 0: #if you're before the first point
        return None #return None

    pointIndex = getPreviousPointIndex(points, time) #get the index of the previous timing point
    if pointIndex == -1: #if you're before the first point
        point = points[0] #get the first point
        timeUntilPoint = point.time - time #get the time until the first point
        dividedBeatLength = point.beatLength / divisor #get the length of a subdivided beat
        beatsUntil = timeUntilPoint / dividedBeatLength #get the beats until the first point
        if isOnBeat(time, point, divisor, True): #if you're on a beat
            realBeatsUntil = round(beatsUntil) - 1 #then beatsUntil would calculate to this time, so subtract 1
            timeOfNextBeat = -realBeatsUntil * dividedBeatLength + point.time #calculate the time of the previous beat based on the real beats until
        else: #else you're not on a beat
            flooredBeatsUntil = math.floor(beatsUntil) #floor beats until to round down to the next beat
            timeOfNextBeat = -flooredBeatsUntil * dividedBeatLength + point.time #calculate the time of the previous beat based on the floored beats until
        return timeOfNextBeat #return the time of the previous beat
    
    point = points[pointIndex] #else you're not before the first timing point
    
    if point.time == time: #if you're on a point        
        newPointIndex = pointIndex #the index of the new timing point to care about
        nextPoint = points[newPointIndex] #the timing point
        while newPointIndex < len(points): #find the latest point with the same time
            nextPoint = points[newPointIndex] #get the point corresponding to the index
            
            if nextPoint.time != time: #if its a different time
                newPointIndex -= 1 #went too far, go back one
                nextPoint = points[newPointIndex] #set the point
                break #break
            
            newPointIndex += 1 #else increment the index
        
        dividedBeatLength = nextPoint.beatLength / divisor #length of a subdivided beat
        timeOfNextBeat = dividedBeatLength + nextPoint.time #calculate the time of the next beat based on the divided beat length
        
        if len(points) > newPointIndex + 1: #if the beat found surpasses the time of the next point
            nextPoint = points[newPointIndex + 1] #get the next point
            if timeOfNextBeat > nextPoint.time: #if the beat found surpasses the time of the next point
                timeOfNextBeat = nextPoint.time #set the time of the next beat to the time of the next point
                
        return timeOfNextBeat #else return the time of the next beat

    timeSincePoint = time - point.time #else you're not on a point, so get the time since the previous timing point
    dividedBeatLength = point.beatLength / divisor #length of a subdivided beat
    beatsElapsed = timeSincePoint / dividedBeatLength #beats elapsed since the previous timing point
    if isOnBeat(time, point, divisor): #if you're on a beat
        realBeatsElapsed = round(beatsElapsed) + 1 #then beatsElapsed would calculate to this time, so add 1
        timeOfNextBeat = realBeatsElapsed * dividedBeatLength + point.time #calculate the time of the next beat based on the real beats elapsed
    else: #else you're not on a beat
        ceiledBeatsElapsed = math.ceil(beatsElapsed) #ceil beats elapsed to round up to the next beat
        timeOfNextBeat = ceiledBeatsElapsed * dividedBeatLength + point.time #calculate the time of the next beat based on the ceiled beats elapsed
    
    if len(points) > pointIndex + 1: #if there is a next point
        nextPoint = points[pointIndex + 1] #get it
        if timeOfNextBeat > nextPoint.time: #if the beat found surpasses the time of the next point
            timeOfNextBeat = nextPoint.time #set the time of the next beat to the time of the next point
    
    return timeOfNextBeat #return the time of the next beat

def getNearestBeat(points, time, divisor): #returns the time of the nearest beat
    def getCloserBeat(previous, next, time): #returns either previous or next, depending on which is closer to time
        if abs(previous - time) < abs(next - time): #if previous is closer
            return previous #return previous
        return next #else return next
    
    if len(points) == 0: #if there are no timing points
        return None #return None
    
    pointIndex = getPreviousPointIndex(points, time) #get the index of the previous timing point
    if pointIndex == -1: #if you're before the first point
        point = points[0] #get the first point
        timeUntilPoint = point.time - time #get the time until the first point
        dividedBeatLength = point.beatLength / divisor #get the length of a subdivided beat
        beatsUntil = timeUntilPoint / dividedBeatLength #get the beats until the first point
        if isOnBeat(time, point, divisor, True): #if you're on a beat
            return time #then you're on a beat so return the time
        previousBeat = getPreviousBeat(points, time, divisor) #else get the previous beat
        nextBeat = getNextBeat(points, time, divisor) #and get the next beat
        return getCloserBeat(previousBeat, nextBeat, time) #and return the closer beat out of the two
    
    point = points[pointIndex] #else you're not before the first timing point
    
    timeSincePoint = time - point.time #time since the previous timing point
    dividedBeatLength = point.beatLength / divisor #length of a subdivided beat
    beatsElapsed = timeSincePoint / dividedBeatLength #beats elapsed since the previous timing point
    if isOnBeat(time, point, divisor): #if you're on a beat
        return time #then you're on a beat so return the time
    previousBeat = getPreviousBeat(points, time, divisor) #else get the previous beat
    nextBeat = getNextBeat(points, time, divisor) #and get the next beat
    return getCloserBeat(previousBeat, nextBeat, time) #and return the closer beat out of the two
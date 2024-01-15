# external imports
import math #math
import intervaltree

class AnimEvent:
    def __init__(self, startTime, endTime, callback, data=None):
        self.startTime = float(startTime) #the time that this animation starts
        self.endTime = float(endTime) #the time it ends
        self.callback = callback #the function it calls
        self.data = data #any additional data
        
class Animation:
    def __init__(self, events, timeSourceTime, repeatType = "oneShot", length = None, ignoreSameTimeUpdates = False):
        #construct the intervalTree that stores all of the anim events
        intervals = []
        for i in events:
            if i.startTime <= i.endTime: #validate that the event has a length
                intervals.append(self.toInterval(i))
        self.tree = intervaltree.IntervalTree(intervals)
        
        #the time source time that this animation started at
        #so it can be subtracted from times that are passed in later
        self.timeSourceStartTime = float(timeSourceTime)
        self.animTime = None
        
        #if the animation should loop or ping pong
        self.repeatType = repeatType
        
        #the length of the animation, set automatically if it is not passed in
        if length is None:
            self.length = self.tree.end()
        else:
            self.length = max(self.tree.end(), length)
        
        #if the animation should ignore updates that don't change the time
        self.ignoreSameTimeUpdates = ignoreSameTimeUpdates
    
    #turns an AnimEvent into an intervaltree.Interval
    def toInterval(self, event):
        return intervaltree.Interval(event.startTime, math.nextafter(event.endTime, float("inf")), (event.callback, event.data))
    
    #adds an event to the animation
    def addEvent(self, event):
        if event.startTime <= event.endTime: #validate
            self.tree.add(self.toInterval(event))
    
    #removes an event from the animation
    def removeEvent(self, event):
        if event.startTime <= event.endTime: #validate
            self.tree.remove(self.toInterval(event))
    
    #gets all of the events that are happening at a certain time
    def getEventsAt(self, time):
        return self.tree.at(time)
    
    #updates the animation
    def updateTime(self, timeSourceTime, *args): #args are passed to the callbacks  
        oldAnimTime = self.animTime #the time that the animation was at before this update
        
        animTimeUnrepeated = float(timeSourceTime) - self.timeSourceStartTime
        match self.repeatType: #set animTime based on the repeat type
            case "loop":
                self.animTime = animTimeUnrepeated % self.length
            case "pingPong":
                self.animTime = abs(animTimeUnrepeated % (self.length * 2) - self.length)
            case _:
                self.animTime = animTimeUnrepeated
        
        #set oldAnimTime to 
        if oldAnimTime is None:
            oldAnimTime = 0.
            if oldAnimTime == self.animTime:
                oldAnimTime = math.nextafter(0., -1.)
                
        if self.ignoreSameTimeUpdates and self.animTime == oldAnimTime:
            return
        
        if self.animTime > oldAnimTime:
            for i in self.tree.overlap(math.nextafter(oldAnimTime, float("inf")), self.animTime):
                if self.animTime <= i.end:
                    continue
                i.data[0](i.end - i.begin, *args)
        else:
            for i in self.tree.overlap(self.animTime, oldAnimTime):
                if self.animTime >= i.begin:
                    continue
                i.data[0](0., *args)
        
        for i in self.tree.at(self.animTime):
            i.data[0](self.animTime - i.begin, *args)
    
    def skipToTime(self, animTime, timeSourceTime):
        self.animTime = animTime
        self.timeSourceStartTime = timeSourceTime - animTime
    
    def restart(self, timeSourceTime):
        self.skipToTime(0, timeSourceTime)
        
def interp(startingValue, endingValue, startingTime, endingTime, basis, currentTime): #Clamps currentTime to the range (startingTime, endingTime)
    d = startingTime
    k = endingTime
    c = startingValue
    a = endingValue
    basisVal = (currentTime - d) / (k - d)
    basisVal = min(max(0, basisVal), 1)
    return (a - c) * basis(basisVal) + c

def lerp(startingValue, endingValue, startingTime, endingTime, currentTime):
    return (currentTime - startingTime) * ((endingValue - startingValue) / (endingTime - startingTime)) + startingValue

def easeInSinBasis(x):
    return math.sin(0.5 * math.pi * (x - 1)) + 1
def easeInSin(startingValue, endingValue, startingTime, endingTime, currentTime):
    return interp(startingValue, endingValue, startingTime, endingTime, easeInSinBasis, currentTime)

def easeOutSinBasis(x):
    return math.sin(0.5 * math.pi * x)
def easeOutSin(startingValue, endingValue, startingTime, endingTime, currentTime):
    return interp(startingValue, endingValue, startingTime, endingTime, easeOutSinBasis, currentTime)

def easeInOutSinBasis(x):
    return math.sin(math.pi * (x - 0.5)) * 0.5 + 0.5
def easeInOutSin(startingValue, endingValue, startingTime, endingTime, currentTime):
    return interp(startingValue, endingValue, startingTime, endingTime, easeInOutSinBasis, currentTime)

def easeInPowBasis(x, pow):
    return math.pow(x, pow)
def easeInPow(startingValue, endingValue, startingTime, endingTime, pow, currentTime):
    return interp(startingValue, endingValue, startingTime, endingTime, lambda x: easeInPowBasis(x, pow), currentTime)

def easeOutPowBasis(x, pow):
    return math.pow(x, 1 / pow)

def easeOutPow(startingValue, endingValue, startingTime, endingTime, pow, currentTime):
    return interp(startingValue, endingValue, startingTime, endingTime, lambda x: easeOutPowBasis(x, pow), currentTime)

def easeInOutPowBasis(x, pow):
    return 0.5 * (math.pow(abs(2 * x - 1), pow) * math.copysign(1, x - 0.5)) + 0.5
def easeInOutPow(startingValue, endingValue, startingTime, endingTime, pow, currentTime):
    return interp(startingValue, endingValue, startingTime, endingTime, lambda x: easeInOutPowBasis(x, pow), currentTime)
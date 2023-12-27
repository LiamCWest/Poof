import math
import intervaltree

class AnimEvent:
    def __init__(self, startTime, endTime, callback, data=None):
        self.startTime = float(startTime)
        self.endTime = float(endTime)
        self.callback = callback
        self.data = data
        
class Animation:
    def __init__(self, events, timeSourceTime, repeatType = "oneShot", length = None, ignoreSameTimeUpdates = False):
        intervals = []
        for i in events:
            if i.startTime <= i.endTime:
                intervals.append(intervaltree.Interval(i.startTime, math.nextafter(i.endTime, float("inf")), (i.callback, i.data)))
        self.tree = intervaltree.IntervalTree(intervals)
        
        self.timeSourceStartTime = float(timeSourceTime)
        self.animTime = None
        
        self.repeatTime = repeatType
        
        if length is None:
            self.length = self.tree.end()
        else:
            self.length = max(self.tree.end(), length)
            
        self.ignoreSameTimeUpdates = ignoreSameTimeUpdates
        
    def getEventsAt(self, time):
        return self.tree.at(time)
        
    def updateTime(self, timeSourceTime, *args):        
        oldAnimTime = self.animTime
        
        animTimeUnrepeated = float(timeSourceTime) - self.timeSourceStartTime
        match self.repeatTime:
            case "loop":
                self.animTime = animTimeUnrepeated % self.length
            case "pingPong":
                self.animTime = abs(animTimeUnrepeated % (self.length * 2) - self.length)
            case _:
                self.animTime = animTimeUnrepeated
                
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
        print(self.animTime, self.timeSourceStartTime)
    
    def restart(self, timeSourceTime):
        self.skipToTime(0, timeSourceTime)
        
def interp(startingValue, endingValue, startingTime, endingTime, basis, currentTime):
    d = startingTime
    k = endingTime
    c = startingValue
    a = endingValue
    return (a - c) * basis((currentTime - d) / (k - d)) + c

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
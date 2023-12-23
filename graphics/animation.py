import math

class AnimEvent:
    def __init__(self, startTime, endTime, callback):
        self.startTime = float(startTime)
        self.endTime = float(endTime)
        self.callback = callback
        
class Animation:
    def __init__(self, events, timeSourceTime, repeatType = "oneShot", length = None):
        self.events = events
        
        self.timeSourceStartTime = timeSourceTime
        self.animTime = None
        
        self.repeatTime = repeatType
        
        if length is None:
            self.length = max(i.endTime for i in self.events)
        else:
            self.length = length
        
    def updateTime(self, timeSourceTime):
        firstUpdate = self.animTime is None
        
        oldAnimTime = self.animTime
        
        animTimeUnrepeated = timeSourceTime - self.timeSourceStartTime
        match self.repeatTime:
            case "loop":
                self.animTime = animTimeUnrepeated % self.length
            case "pingPong":
                self.animTime = abs(animTimeUnrepeated % (self.length * 2) - self.length)
            case _:
                self.animTime = animTimeUnrepeated

        if firstUpdate:
            oldAnimTime = self.animTime
        
        if self.animTime > oldAnimTime or firstUpdate:
            for event in self.events:
                if event.endTime < event.startTime:
                    continue
                
                if event.endTime < self.animTime and event.endTime > oldAnimTime: #event has now ended but had not ended last update
                    event.callback(event.endTime - event.startTime)
                elif event.startTime <= self.animTime <= event.endTime: #if event is playing
                    event.callback(self.animTime - event.startTime)
        elif self.animTime < oldAnimTime:
            for event in self.events:
                if event.endTime < event.startTime:
                    continue
                
                if event.startTime > self.animTime and event.startTime < oldAnimTime: #event has not started but had started last update
                    event.callback(0)
                elif event.startTime <= self.animTime <= event.endTime: #if event is playing
                    event.callback(self.animTime - event.startTime)
    
    def skipToTime(self, animTime, timeSourceTime):
        self.animTime = animTime
        self.timeSourceStartTime = timeSourceTime - animTime
    
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
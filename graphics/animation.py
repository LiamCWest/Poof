import utils.binarySearch

class AnimEvent:
    def __init__(self, startTime, endTime, callback):
        self.startTime = startTime
        self.endTime = endTime
        self.callback = callback
        
class Animation:
    def __init__(self, events, timeSourceTime):
        self.events = events
        
        self.timeSourceStartTime = timeSourceTime
        self.animTime = 0
        self.eventsRunning = []
        
    def updateTime(self, timeSourceTime):
        oldAnimTime = self.animTime
        self.animTime = timeSourceTime - self.timeSourceStartTime
        
        
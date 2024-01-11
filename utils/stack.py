class Stack:
    def __init__(self, maxSize = None):
        self.maxSize = maxSize
        self.top = 0
        self.items = []
        
    def push(self, item):
        if self.maxSize and len(self.items) >= self.maxSize:
            print("Stack Overflow")
        else:
            self.items.append(item)
            self.top += 1
        
    def pop(self):
        if len(self.items) <= 0:
            print("Stack Underflow")
            return None
        else:
            self.top -= 1
            return self.items.pop()
    
    def peek(self):
        return self.items[self.top] if len(self.items) > 0 else None
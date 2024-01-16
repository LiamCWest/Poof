#a stack, a last in first out data structure

class Stack: #the stack class
    def __init__(self, maxSize = None): #constructor
        self.maxSize = maxSize #the maximum size of the stack
        self.top = 0 #the index of the top of the stack
        self.items = [] #the items in the stack
        
    def push(self, item): #pushes an item to the stack
        if self.maxSize and len(self.items) >= self.maxSize: #if the stack is full
            print("Stack Overflow") #print that the stack is full
        else: #if the stack is not full
            self.items.append(item) #add the item to the stack
            self.top += 1 #increment the top of the stack
        
    def pop(self): #pops an item from the stack
        if len(self.items) <= 0: #if the stack is empty
            print("Stack Underflow") #print that the stack is empty
            return None #return None
        else: #if the stack is not empty
            self.top -= 1 #decrement the top of the stack
            return self.items.pop() #return the item popped from the stack
    
    def peek(self): #returns the item on the top of the stack
        return self.items[self.top] if len(self.items) > 0 else None #return the item on the top of the stack if the stack is not empty, otherwise return None
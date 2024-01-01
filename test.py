class test:
    def __init__(self):
        self.val = 3
        
    def returnVal(self):
        def inner():
            return self.val
        
        return inner()
    
t = test()
print(t.returnVal())
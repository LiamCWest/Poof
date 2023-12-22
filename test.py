class superc:
    def __init__(self, value):
        print(2)
        print(value)
        
    def printValue(self):
        print(2)

class subc(superc):
    def __init__(self, value):
        super().__init__(value)
        
i = subc(3)

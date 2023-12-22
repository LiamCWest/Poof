class superc:
    def __init__(self, value):
        self.thing = value

class subc:
    def __init__(self, value):
        self.renamedThing = value
        super().__init__()
        
        print(self.thing)
        
i = subc(3)

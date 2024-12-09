

_list = []

class Peripheral:
    def __init__(self):
        if type(self) is Peripheral:
            raise TypeError("Peripheral cannot be instantiated directly")
        
        _list.append(self)
    
    def reset(self):
        pass
    
    def debug(self):
        # print(f"Peripheral debug: {self}")
        pass

def reset_all():
    for p in _list:
        p.reset()

def debug_all():
    for p in _list:
        p.debug()




_peripherals = []


class Peripheral:
    def __init__(self):
        if type(self) is Peripheral:
            raise TypeError("Peripheral cannot be instantiated directly")
        
        _peripherals.append(self)
    
    def reset(self):
        print(f"Peripheral reset:{self}")

def reset():
    print("Resetting device")
    for p in _peripherals:
        p.reset()


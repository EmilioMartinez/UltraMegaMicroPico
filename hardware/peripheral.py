

class Peripheral:
    def __init__(self):
        if type(self) is Peripheral:
            raise TypeError("Peripheral cannot be instantiated directly")
        
        from hardware.device import device
        device.register_peripheral(self)
    
    def reset(self):
        print(f"Peripheral reset:{self}")


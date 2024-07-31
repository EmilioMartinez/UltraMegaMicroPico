

<<<<<<<< HEAD:peripherals/peripheral.py
_list = []

========
>>>>>>>> c0a2b5b63425ca81cf4d1bb99c311fa2d7bc4d5c:hardware/peripheral.py
class Peripheral:
    def __init__(self):
        if type(self) is Peripheral:
            raise TypeError("Peripheral cannot be instantiated directly")
        
<<<<<<<< HEAD:peripherals/peripheral.py
        _list.append(self)
========
        from hardware.device import device
        device.register_peripheral(self)
>>>>>>>> c0a2b5b63425ca81cf4d1bb99c311fa2d7bc4d5c:hardware/peripheral.py
    
    def reset(self):
        print(f"Peripheral reset:{self}")

<<<<<<<< HEAD:peripherals/peripheral.py
def reset_all():
    for p in _list:
        p.reset()

========
>>>>>>>> c0a2b5b63425ca81cf4d1bb99c311fa2d7bc4d5c:hardware/peripheral.py

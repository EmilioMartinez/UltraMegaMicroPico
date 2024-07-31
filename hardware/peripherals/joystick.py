from peripherals.peripheral import Peripheral
from machine import ADC, Pin
<<<<<<<< HEAD:peripherals/joystick.py
========
from hardware.peripheral import Peripheral
>>>>>>>> c0a2b5b63425ca81cf4d1bb99c311fa2d7bc4d5c:hardware/peripherals/joystick.py


class Joystick(Peripheral):
    def __init__(self, pin_x, pin_y, pin_button, deadzone=3000):
        super().__init__()
        self.axis_x = Joystick.Axis(pin_x, deadzone)
        self.axis_y = Joystick.Axis(pin_y, deadzone)
        self.button = Pin(pin_button, Pin.IN, Pin.PULL_UP)

    def read(self):
        x = self.axis_x.sample()
        y = self.axis_y.sample()
        b = not self.button.value()
        return x, y, b

    def debug(self):
        print(f"Joystick: {self.read()}")
    
    class Axis:
        def __init__(self, pin, deadzone):
            self.adc = ADC(Pin(pin))
            self.deadzone = deadzone
        
        def sample(self):
            raw = self.adc.read_u16()
            d = self.deadzone
            max = 32767
            if raw < max - d:
                return -(raw - (max - d))/(max - d)
            elif raw > max + d:
                return -(raw - (max + d))/(max - d)
            else:
                return 0


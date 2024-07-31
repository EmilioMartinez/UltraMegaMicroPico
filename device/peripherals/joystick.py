from machine import ADC, Pin
from device.device import Peripheral


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


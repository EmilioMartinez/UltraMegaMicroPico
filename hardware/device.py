from hardware.peripherals.graphics.ST7735_controller import ST7735_Controller
from hardware.peripherals.audio.buzzer import Buzzer
from hardware.peripherals.joystick import Joystick

class Device:
    def __init__(self):
        global device
        device = self
        self._peripherals = []
        
        self.joystick = Joystick(26, 27, 0)
        self.audio = Buzzer(1)
        self.graphics = ST7735_Controller(14, 15, 16, 17, 18)
        

    def register_peripheral(self, p):
        self._peripherals.append(p)

    def reset(self):
        print("Resetting device")
        for p in self._peripherals:
            p.reset()


device = Device()


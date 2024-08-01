from peripherals.peripheral import Peripheral
from machine import ADC, Pin
import uasyncio


class RotaryEncoder(Peripheral):
    def __init__(self, pin):
        super().__init__()
        self.pin1 = Pin(pin)
        self.pin2 = Pin(pin, Pin.IN, Pin.PULL_UP)

    def debug(self):
        super().debug()
        print(self.read())

    def read(self):
        return self.pin1.value()
    

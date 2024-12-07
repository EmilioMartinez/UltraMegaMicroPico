from . import Peripheral
from machine import Pin
import uasyncio


class RotaryEncoder(Peripheral):
    def __init__(self, clk_pin, dt_pin, sw_pin=None):
        self.pin_clk = Pin(clk_pin, Pin.IN, Pin.PULL_UP)
        self.pin_dt  = Pin(dt_pin , Pin.IN, Pin.PULL_UP)
        self.pin_sw  = Pin(sw_pin , Pin.IN, Pin.PULL_UP) if sw_pin is not None else None

        self.last_clk_state = self.pin_clk.value()
        self.last_dt_state  = self.pin_dt .value()
        self.counter = 0
        self._rotary_task = None
        self._button_task = None

    def debug(self):
        super().debug()
        print(self.pin_clk.value(), self.pin_dt.value(), (self.pin_sw.value() if self.pin_sw else None))
        print(self.get_counter())

    async def _rotary_encoder(self):
        while True:
            clk_state = self.pin_clk.value()
            dt_state = self.pin_dt.value()

            if clk_state != self.last_clk_state:
                if clk_state == 0:
                    if dt_state != clk_state:
                        self.counter += 1
                    else:
                        self.counter -= 1
                    print('Counter:', self.counter)

            self.last_clk_state = clk_state
            self.last_dt_state = dt_state
            await uasyncio.sleep(0)  # Yield control to other tasks

    async def _button_handler(self):
        while True:
            if self.pin_sw and not self.pin_sw.value():  # If button is pressed (active low)
                print('Button pressed!')
                while not self.pin_sw.value():
                    await uasyncio.sleep(0)  # Wait until the button is released
            await uasyncio.sleep(0)  # Check button state periodically

    def start(self):
        self._rotary_task = uasyncio.create_task(self._rotary_encoder())
        if self.pin_sw:
            self._button_task = uasyncio.create_task(self._button_handler())

    def stop(self):
        if self._rotary_task:
            self._rotary_task.cancel()
        if self._button_task:
            self._button_task.cancel()

    def get_counter(self):
        return self.counter


from . import Peripheral
from machine import Pin
import uasyncio


# Consider CLK and DT as axi of the plane, then we have the four points:
# (calling them Quadrants is a stretch though)
# Quadrant | (CLK, DT)
#        0 | (0, 0)
#        1 | (1, 0)
#        2 | (1, 1)
#        3 | (0, 1)
# Quadrant changes are counted.
# A click is made of 4 counters
# A turn is made of clicks_per_turn clicks
# Clicks are discretized, while turns are though as a continuum
# The phase is simply floor(get_turns)
# Skipping a quadrant raises an exception by default, but can be set to be flexible by setting strict_counting to false

class RotaryEncoder(Peripheral):
    def __init__(self, clk_pin, dt_pin, sw_pin=None, strict_counting=True, clicks_per_turn=None):
        self._pin_clk = Pin(clk_pin, Pin.IN, Pin.PULL_UP)
        self._pin_dt  = Pin(dt_pin , Pin.IN, Pin.PULL_UP)
        self._pin_sw  = Pin(sw_pin , Pin.IN, Pin.PULL_UP) if sw_pin is not None else None
        self._strict_counting = strict_counting
        self._clicks_per_turn = clicks_per_turn

        # Initial state
        self._quadrant = self._get_quadrant()
        self._counter = 0
        
        self.debug()

        self._update_task = uasyncio.create_task(self._update_coroutine())
        # set up interrupts

    def _get_quadrant(self) -> int:
        clk = self._pin_clk.value()
        dt  = self._pin_dt .value()
        return 2 * clk + clk ^ dt

    def get_counter(self) -> int:
        return self._counter

    def get_clicks(self) -> int:
        return self._counter//4
    
    def get_turns(self) -> float:
        if self._clicks_per_turn is None:
            raise AttributeError("No clicks_per_turn not set")

        return self._counter/(4 * self._clicks_per_turn)
    
    def debug(self):
        super().debug()
        print(f"quadrant: {self._get_quadrant()}, clk: {self._pin_clk.value()}, dt: {self._pin_dt.value()}"
            +   (f", sw: {self._pin_sw.value()}" if self._pin_sw else "")
            +   f", counter: {self.get_counter()}, clicks: {self.get_clicks()}"
            +   (f", turns: {self.get_turns()}" if self._clicks_per_turn is not None else "")
            )

    async def _update_coroutine(self):
        while True:
            new_quadrant = self._get_quadrant()
            diff = (new_quadrant - self._quadrant) % 4

            if diff == 1:
                self._counter += 1
            if diff == 3:
                self._counter -= 1
            if diff == 2:
                if self._strict_counting:
                    print("--- Quadrant was skipped, debugging before raising error:")
                    self.debug()
                    raise ValueError("Invalid encoder state, quadrant was skipped")
            
            self._quadrant = new_quadrant

            self.debug()
            await uasyncio.sleep(0)

    def reset(self):
        super().reset()
        if self._update_task:
            self._update_task.cancel() # type: ignore
            self._update_task = None


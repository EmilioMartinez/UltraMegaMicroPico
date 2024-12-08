from . import Peripheral
from machine import Pin
from micropython import schedule


# This rotary encoder ignores the usual switch button
# If present, it should be treated as a regular button on an unrelated pin

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
    def __init__(self, clk_pin, dt_pin, strict_counting=True, clicks_per_turn=None):
        self._pin_clk = Pin(clk_pin, Pin.IN, Pin.PULL_UP)
        self._pin_dt  = Pin(dt_pin , Pin.IN, Pin.PULL_UP)
        self._strict_counting = strict_counting
        self._clicks_per_turn = clicks_per_turn

        # Initial state
        self._quadrant = self._get_quadrant()
        self._counter = 0
        
        self._pin_clk.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._handle_interrupt)
        self._pin_dt .irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._handle_interrupt)

    def _get_quadrant(self) -> int:
        clk = self._pin_clk.value()
        dt  = self._pin_dt .value()
        return 2 * clk + clk ^ dt

    def get_counter(self) -> int:
        return self._counter

    def get_clicks(self) -> int:
        return self._counter // 4
    
    def get_turns(self) -> float:
        if self._clicks_per_turn is None:
            raise AttributeError("clicks_per_turn not set")
        return self._counter / (4 * self._clicks_per_turn)

    def _handle_interrupt(self, pin):
        schedule(self._update, None)

    def _update(self, _):
        new_quadrant = self._get_quadrant()
        diff = (new_quadrant - self._quadrant) % 4

        if diff == 1:
            self._counter += 1
        elif diff == 3:
            self._counter -= 1
        elif diff == 2 and self._strict_counting:
            print("--- Quadrant was skipped, debugging before raising error:")
            self.debug()
            raise ValueError("Invalid encoder state, quadrant was skipped")
        
        self._quadrant = new_quadrant
        self.debug()
    
    def debug(self):
        super().debug()
        print(f"quadrant: {self._get_quadrant()}, clk: {self._pin_clk.value()}, dt: {self._pin_dt.value()}"
            + f", counter: {self.get_counter()}, clicks: {self.get_clicks()}"
            + (f", turns: {self.get_turns()}" if self._clicks_per_turn is not None else "")
        )

    def reset(self):
        super().reset()
        self._pin_clk.irq(None)
        self._pin_dt .irq(None)


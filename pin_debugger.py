from machine import Pin
import uasyncio
import utils

ALL_INDICES = range(30)
DEFAULT_SELECTION = ALL_INDICES

# Create all pins anyways so as to keep indexing neat
_pins = [Pin(i) for i in ALL_INDICES]
_interval = 1.0

def debug_pins(*sel):
    selected = DEFAULT_SELECTION if not sel else sel[0] if utils.is_iterable(sel[0]) else sel
    values_iter = (f"{i}: {_pins[i].value()}" for i in selected)
    print("Pin values: " + ", ".join(values_iter))

def set_interval(new):
    global _interval
    _interval = new

async def debug_pins_auto(*selected):
    while True:
        debug_pins(*selected)
        await uasyncio.sleep(_interval)


try:
    uasyncio.run(debug_pins_auto(0, 1, 2, 3, 4))
except KeyboardInterrupt:
    pass


from machine import Pin
import uasyncio
import utils

ALL_INDICES = range(30)
DEFAULT_SELECTION = ALL_INDICES

# Create all pins anyways so as to keep indexing neat
_pins = [Pin(i) for i in ALL_INDICES]
_interval = 1.0

def value(i):
    return _pins[i].value()

def set_interval(new_interval):
    global _interval
    _interval = new_interval

def debug_pins(*selected):
    selected = DEFAULT_SELECTION if not selected else selected[0] if utils.is_iterable(selected[0]) else selected
    values_iter = (f"{i}: {'Off' if value(i) else 'On '}" for i in selected)
    print("Pin values: " + ", ".join(values_iter))

async def auto_debug_pins():
    # maybe revert to array to keep ordered
    tracked = set()
    while True:
        tracked.update(i for i in ALL_INDICES if not value(i))
        debug_pins(tracked)
        await uasyncio.sleep(_interval)


try:
    uasyncio.run(auto_debug_pins())
except KeyboardInterrupt:
    pass


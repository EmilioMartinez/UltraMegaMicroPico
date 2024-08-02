from machine import Pin
import uasyncio
import utils.utils as utils

ALL_INDICES = range(30)
DEFAULT_SELECTION = ALL_INDICES

# Create all pins anyways so as to keep indexing neat
_pins = [Pin(i, Pin.IN, Pin.PULL_UP) for i in ALL_INDICES]
_interval = 1.0

def pressed(i):
    return not _pins[i].value()

def set_interval(new_interval):
    global _interval
    _interval = new_interval

def debug_pins(*selected):
    selected = DEFAULT_SELECTION if not selected else selected[0] if utils.is_iterable(selected[0]) else selected
    values_iter = (f"{i}: {'On ' if pressed(i) else 'Off'}" for i in selected)
    print("Pin values: " + ", ".join(values_iter))

async def auto_debug_pins():
    tracked = [False for i in ALL_INDICES]
    while True:
        for i in ALL_INDICES:
            if pressed(i):
                tracked[i] = True
        debug_pins(i for i in ALL_INDICES if tracked[i])
        await uasyncio.sleep(_interval)

def start_auto_debug_task():
    uasyncio.create_task(auto_debug_pins())


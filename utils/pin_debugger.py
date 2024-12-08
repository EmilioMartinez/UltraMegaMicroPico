from machine import Pin
import uasyncio
import utils.utils as utils

ALL_INDICES = range(30)
DEFAULT_SELECTION = ALL_INDICES

# Create all pins anyways so as to keep indexing neat
_pins = [Pin(i) for i in ALL_INDICES]
_interval = 1.0

def pressed(i):
    return _pins[i].value()

def set_interval(new_interval):
    global _interval
    _interval = new_interval

def debug_pins(*selected):
    selected = DEFAULT_SELECTION if not selected else selected[0] if utils.is_iterable(selected[0]) else selected
    values_iter = (f"{i}: {'On ' if pressed(i) else 'Off'}" for i in selected)
    print("Pin values: " + ", ".join(values_iter))

async def _auto_debug_selected_coroutine(*selected):
    while True:
        debug_pins(*selected)
        await uasyncio.sleep(_interval)

async def _auto_debug_tracked_coroutine():
    tracked = [False for i in ALL_INDICES]
    while True:
        for i in ALL_INDICES:
            if pressed(i):
                tracked[i] = True
        debug_pins(i for i in ALL_INDICES if tracked[i])
        await uasyncio.sleep(_interval)

def start_auto_debug_task(*selected):
    coro = _auto_debug_selected_coroutine(*selected) if selected else _auto_debug_tracked_coroutine()
    uasyncio.create_task(coro)
    return coro


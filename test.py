import uasyncio
import pin_debugger


try:
    uasyncio.run(pin_debugger.debug_pins_interval())
except KeyboardInterrupt:
    pass


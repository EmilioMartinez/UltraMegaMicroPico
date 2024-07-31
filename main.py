import uasyncio
<<<<<<< HEAD
import device
=======
from hardware.device import device
>>>>>>> c0a2b5b63425ca81cf4d1bb99c311fa2d7bc4d5c
import apps.menu

async def main():
    await apps.menu.run()

try:
    print("Main loop initiated")
    main_loop = main()
    uasyncio.run(main_loop)
except KeyboardInterrupt:
    # Here go debug methods
    # Here go termination methods
    main_loop.close()
    print("Main loop terminated")
    device.reset()


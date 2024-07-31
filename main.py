import uasyncio
from hardware.device import device
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


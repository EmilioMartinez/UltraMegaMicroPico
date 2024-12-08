import device
import uasyncio
import apps
import utils.pin_debugger as pin_debugger


coroutines = set()

async def main():
    coroutines.add(pin_debugger.start_auto_debug_task())
    await uasyncio.sleep(300000)
    # await apps.loader()

try:
    print("Main loop initiated")
    main_loop = main()
    uasyncio.run(main_loop)
except KeyboardInterrupt:
    # Here go debug methods
    # Here go pre-termination methods
    main_loop.close()
finally:
    # Here go termination methods
    for coro in coroutines:
        print(f"Canceling: {coro}")
        coro.close()
    print("Main loop terminated")
    device.reset()


import device
import uasyncio
import apps


coroutines = set()

async def print_wheel_data():
    while True:
        print(device.wheel.get_turns())
        await uasyncio.sleep(1)

async def main():
    uasyncio.create_task(print_wheel_data())
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


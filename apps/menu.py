import uasyncio


async def run():
    while True:
        print("zzz...")
        await uasyncio.sleep(1)


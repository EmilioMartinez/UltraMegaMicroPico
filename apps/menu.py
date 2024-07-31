import uasyncio
import device
from peripherals.audio.music import we_are_number_one


async def run():
    device.graphics.write_text((20, 40), "hey there pretty")
    await device.audio.play_score(we_are_number_one, 0.01)

    await uasyncio.sleep(2)
    for i in range(4):
        device.graphics.write_text((60 + 10 * i, 60 + 10 * i), "zzz")
        await device.audio.play_tone(100, 1)
        await uasyncio.sleep(0.4)


from device.peripherals.graphics.ST7735_controller import ST7735_Controller
from device.peripherals.audio.buzzer import Buzzer
from device.peripherals.joystick import Joystick


joystick = Joystick(26, 27, 0)
audio = Buzzer(1)
graphics = ST7735_Controller(14, 15, 16, 17, 18)


try:
    from i2c import I2CTarget
except:
    pass
from animation_test import GradientAnimation
from animation_pulse import PulseAnimation
from animation_rainbow import RainbowAnimation
from animation_greenwhite import GreenWhiteAnimation
from animation_longstrip import LongStripAnimation
from time import sleep
from colors import *
from pixelstrip import PixelStrip, MATRIX_BOTTOM, MATRIX_TOP, MATRIX_LEFT, MATRIX_RIGHT, MATRIX_COLUMN_MAJOR, MATRIX_ZIGZAG
import board

BRIGHTNESS = 0.1

strip = [
    # PixelStrip(width=24,height=1,circle=True),
    PixelStrip(board.GP10, n=24, bpp=4, pixel_order="GRB", brightness=BRIGHTNESS, options={MATRIX_BOTTOM, MATRIX_RIGHT, MATRIX_COLUMN_MAJOR, MATRIX_ZIGZAG}),
    PixelStrip(board.GP12, n=24, bpp=4, pixel_order="GRB", brightness=BRIGHTNESS, options={MATRIX_TOP, MATRIX_LEFT, MATRIX_COLUMN_MAJOR, MATRIX_ZIGZAG}),
    PixelStrip(board.GP14, n=24, bpp=4, pixel_order="GRB", brightness=BRIGHTNESS, options={MATRIX_TOP, MATRIX_LEFT, MATRIX_COLUMN_MAJOR, MATRIX_ZIGZAG}),
    PixelStrip(board.GP16, n=24, bpp=4, pixel_order="GRB", brightness=BRIGHTNESS, options={MATRIX_TOP, MATRIX_LEFT, MATRIX_COLUMN_MAJOR, MATRIX_ZIGZAG}),
    PixelStrip(board.GP18, n=81, bpp=4, pixel_order="GRB", brightness=BRIGHTNESS, options={MATRIX_TOP, MATRIX_LEFT, MATRIX_COLUMN_MAJOR, MATRIX_ZIGZAG}),
    PixelStrip(board.GP19, n=81, bpp=4, pixel_order="GRB", brightness=BRIGHTNESS, options={MATRIX_TOP, MATRIX_LEFT, MATRIX_COLUMN_MAJOR, MATRIX_ZIGZAG}),
]

animation = [
    GreenWhiteAnimation(),
    GreenWhiteAnimation(),
    GreenWhiteAnimation(),
    GreenWhiteAnimation(),
    LongStripAnimation(),
    LongStripAnimation()
]

i2c = None

def receive_message():
    """
    Receive a message through I2C, if available.  The first byte will
    contain the strip number and animation number, packed into the single
    byte.  If there is a param associated with this message, it is 
    concatenated after the first byte.
    """
    global i2c
    if i2c is None:
        return None
    message = i2c.request()
    if not message:
        return None
    with message:
        message_bytes = message.read()
        b = message_bytes[0]
        strip_num = int((b & 0xE0) >> 5)
        anim_num = int(b & 0x1F)
        param = None 
        if len(message_bytes) > 1:
            param = message_bytes[1:].decode('utf-8')
        print(f"received {len(message_bytes)} bytes      {(strip_num, anim_num, param)}")
        return (strip_num, anim_num, param)
    return None

def main(): 
    "Main program loop, for reading messages and changing Animations." 
    global strip, led
    last_msg_time = 0.0
    strip[0].animation = animation[0] 
    strip[1].animation = animation[1]
    strip[2].animation = animation[2]
    strip[3].animation = animation[3]
    while True:
        for s in strip:
            s.draw()
        message = receive_message()
        if message is not None:
            strip_num = message[0]
            anim_num = message[1]
            

def blink(n, color=BLUE, sleep_time=0.4): 
    "Blink lights to show that the program is progressing."
    global strip, led
    for s in strip:
        s.clear()
    for _ in range(n):
        for s in strip:
            s[0] = color
            s.show()
            # led.value = True
        sleep(sleep_time)
        for s in strip:
            s.clear()
            s.show()
            # led.value = False
        sleep(sleep_time)


if __name__ == "__main__": 
    # blink(2, BLUE)
    # with I2CTarget(scl=board.SCL, sda=board.SDA, addresses=[I2C_ADDRESS]) as i2c:
    blink(1, GREEN)
    main()

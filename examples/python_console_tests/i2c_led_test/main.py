import time
from smbus import SMBus
import datetime


class KeyboardLed:
    def __init__(self):
        self.i2c = SMBus(1)
        self.i2cadress = 0x20

    def write_single_pixel(self, data: list):
        # format of data: [pixel, r, g, b]
        try:
            self.i2c.write_i2c_block_data(self.i2cadress, 0, data)
        except OSError as e:
            print(str(e) + " => I2C device not found")

    def test_fade_pixel_up_and_down(self, pixel: int):
        for i in range(0, 255):
            self.write_single_pixel([pixel, i, 0, 0])
            time.sleep(0.01)
        for i in range(255, 0, -1):
            self.write_single_pixel([pixel, i, 0, 0])
            time.sleep(0.01)


K = KeyboardLed()

K.write_single_pixel([0, 0, 0, 0])

input("Press Enter to start test...")

K.write_single_pixel([0, 255, 255, 0])

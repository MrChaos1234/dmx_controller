from smbus import SMBus

class I2cLedDriver(object):
    i2c_bus: SMBus
    i2cadress: int
    
    def __init__(self, i2c_bus: SMBus):
        self.i2c_bus = i2c_bus
        self.i2cadress = 0x30
        
    def change_led_color(self, led_number: int, r: int, g: int, b: int):
        data = [led_number, r, g, b]
        print("DRIVER LEVEL: I2cLed.change_led_color() called with arguments: led_number = {}, r = {}, g = {}, b = {}".format(led_number, r, g, b))
        try:
            self.i2c_bus.write_i2c_block_data(self.i2cadress, 0, data)
        except OSError as e:
            print(str(e) + " => I2C device not found")
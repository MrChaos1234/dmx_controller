from RPi import GPIO


class RotaryEncoder(object):
    # Test Rotary encoder (Motherboard Connector 1)
    # A = 17
    # B = 27
    # C = 22
    def __init__(self, clk, dt, pb):
        self.clk = clk
        self.dt = dt
        self.pb = pb

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pb, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.counter = 0
        self.clkLastState = GPIO.input(self.clk)

    def read(self):
        clkState = GPIO.input(self.clk)
        dtState = GPIO.input(self.dt)
        if clkState != self.clkLastState:
            if dtState != clkState:
                self.counter += 1
            else:
                self.counter -= 1
        self.clkLastState = clkState
        return self.counter

    def read_button(self):
        if GPIO.input(self.pb) == 0:
            return True
        else:
            return False

    def set_counter_to_zero(self):
        self.counter = 0




# HOW TO USE:

# RotaryEncoder1 = RotaryEncoder(27, 17, 22)
#
# while True:
#     value = RotaryEncoder1.read()
#     if RotaryEncoder1.read_button():
#         RotaryEncoder1.set_counter_to_zero()
#         value = 0
#     print(value)









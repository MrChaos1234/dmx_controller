from RPi import GPIO

# Test Poti (Motherboard Connector 1)
# A = 17
# B = 27
# C = 22

clk = 27
dt = 17
pb = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pb, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 0
clkLastState = GPIO.input(clk)


while True:
    pbState = GPIO.input(pb)
    if pbState == 0:
        counter = 0

    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    if clkState != clkLastState:
        if dtState != clkState:
            counter += 1
        else:
            counter -= 1
    print(counter)
    clkLastState = clkState



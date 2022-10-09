import time
import sys

from artnet_output import ArtnetOutputter

A = ArtnetOutputter(512)
A.start_output()

time.sleep(1)

while True:
    command_raw: str = input("#")
    command: list = command_raw.split(" ")

    if str(command[0]) == "set" or str(command[0]) == "Set":
        if str(command[1]).isdecimal():
            if int(command[1]) > 512: print("Channel Number out of range")
            else:
                channel = int(command[1])
                if str(command[2]).isdecimal():
                    if int(command[2]) > 255: print("Value out of range")
                    else:
                        value = int(command[2])
                        A.change_value_for_channel(channel, value)

    if str(command[0]) == "exit" or str(command[0]) == "Exit":
        break

A.stop_output()

sys.exit("Done")



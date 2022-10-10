import time
import sys

from artnet_output import ArtnetOutputter
from execute import Executer

E = Executer()

A = ArtnetOutputter(512)
A.start_output()
A.generate_empty_dmx_output_file()
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

    if str(command[0]) == "fixture" or str(command[0]) == "Fixture":
        if str(command[1]).isdecimal():
            fixture_id = int(command[1])

            if str(command[2]) == "color" or str(command[2]) == "Color":
                if "[" not in str(command[3]) or not "]" in str(command[3]): print("Color not in correct format")
                else:
                    color = str(command[3]).strip("[").strip("]").split(",")
                    E.change_rgb_fixture_color(A, fixture_id, color)

            if str(command[2]) == "dimmer" or str(command[2]) == "Dimmer":
                dimmer_value = int(command[3])
                E.change_fixture_dimmer(A, fixture_id, dimmer_value)

    if str(command[0]) == "exit" or str(command[0]) == "Exit":
        break



A.stop_output()

sys.exit("Done")



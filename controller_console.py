import time
import sys

from artnet_manager import ArtnetManager
from execute import Executer
from fixture_manager import FixtureManager
from pult_hardware_manager import PultHardwareManager

E = Executer()
F = FixtureManager()
P = PultHardwareManager()

A = ArtnetManager(512)
A.start_output()
A.generate_empty_dmx_output_file()
time.sleep(1)

print("For help type 'help'")

while True:
    command_raw: str = input("#")
    command: list = command_raw.split(" ")

    if str(command[0]) == "set":
        channel = str(command[1])
        if str(command[2]).isdecimal():
            if int(command[2]) > 255: print("Value out of range")
            else:
                value = int(command[2])
                A.change_value_for_channel(channel, value, False)

    elif str(command[0]) == "fixture":
        if str(command[1]).isdecimal():
            fixture_id = int(command[1])

            if str(command[2]) == "color":
                if "[" not in str(command[3]) or not "]" in str(command[3]): print("Color not in correct format")
                else:
                    color = str(command[3]).strip("[").strip("]").split(",")
                    E.change_rgb_fixture_color(A, fixture_id, color)

            elif str(command[2]) == "dimmer":
                dimmer_value = int(command[3])
                E.change_fixture_dimmer(A, fixture_id, dimmer_value)

            elif str(command[2]) == "shutter":
                shutter_value = int(command[3])
                E.change_fixture_shutter(A, fixture_id, shutter_value)

            else:
                print("Unknown command")

        else:
            print("Unknown command")

    elif str(command[0]) == "add":
        if str(command[1]) == "fixture" or str(command[1]) == "Fixture":
            fixture_library_id = int(command[2])
            mode_id = int(command[3])
            fixture_id = int(command[4])
            fixture_display_name = str(command[5])
            dmx_address = str(command[6])
            F.add_fixture(fixture_library_id, mode_id, fixture_id, fixture_display_name, dmx_address)
        else:
            print("Unknown command")

    elif str(command[0]) == "remove":
        if str(command[1]) == "fixture" or str(command[1]) == "Fixture":
            fixture_id = int(command[2])
            F.remove_fixture(fixture_id)
        else:
            print("Unknown command")

    elif str(command[0]) == "list":
        if str(command[1]) == "fixturelibrary":
            print(F.list_available_fixtures())
        elif str(command[1]) == "dmxpatch":
            print(F.calculate_dmx_patch())
        elif str(command[1]) == "fixturepatch":
            for el in F.calculate_fixture_patch():
                print(F.calculate_fixture_patch()[el])
        else:
            print("Unknown command")

    elif str(command[0]) == "hardware":
        if str(command[1]) == "read":
            if str(command[2]) == "fader":
                fader_id = int(command[3])
                print(P.get_fader_value(fader_id))
            elif str(command[2]) == "button":
                button_id = int(command[3])
                print(P.get_button_value(button_id))
        elif str(command[1]) == "set":
            if str(command[2]) == "fader":
                fader_id = int(command[3])
                value = int(command[4])
                P.set_fader_value(fader_id, value)
        elif str(command[1]) == "map":
            if str(command[2]) == "fader":
                fader_id = int(command[3])
                channel = str(command[4])
                E.start_map_fader_to_channel(A, P, fader_id, channel)
            elif str(command[2]) == "button":
                button_id = int(command[3])
                channel = str(command[4])
                E.start_map_flash_buttons_to_channels(A, P, channel)
        elif str(command[1]) == "unmap":
            if str(command[2]) == "fader":
                fader_id = int(command[3])
                E.stop_map_fader_to_channel(fader_id)
            elif str(command[2]) == "button":
                button_id = int(command[3])
                E.stop_map_flash_buttons_to_channels(button_id)

    elif str(command[0]) == "exit":
        break

    elif str(command[0]) == "help":
        # list all available commands
        print("Available Commands:")
        print("- set (universe.channel) (value)" + " " * 10 + "Sets a channel to a value")
        print("- fixture (fixture_id) color [r,g,b]" + " " * 10 + "Sets a fixture to a color")
        print("- fixture (fixture_id) dimmer (value)" + " " * 10 + "Sets a fixture to a dimmer value")
        print("- fixture (fixture_id) shutter (value)" + " " * 10 + "Sets a fixture to a shutter value")
        print("- add fixture (fixture_library_id) (mode_id) (fixture_id) (fixture_display_name) (universe.channel)" + " " * 10 + "Adds a fixture to the fixture patch")
        print("- remove fixture (fixture_id)" + " " * 10 + "Removes a fixture")
        print("- list fixturelibrary" + " " * 10 + "Lists all available fixtures")
        print("- list fixturepatch" + " " * 10 + "Lists the fixture patch")
        print("- list dmxpatch" + " " * 10 + "Lists all dmx channels")
        print("- hardware read fader (fader_id)" + " " * 10 + "Reads a fader value")
        print("- hardware set fader (fader_id) (value)" + " " * 10 + "Writes a fader value")
        print("- hardware read button (button_id)" + " " * 10 + "Reads a button value")
        print("- hardware map fader (fader_id) (universe.channel)" + " " * 10 + "Maps a fader to a channel")
        print("- hardware unmap fader (fader_id)" + " " * 10 + "Unmaps a fader")
        print("- hardware map button (button_id) (universe.channel)" + " " * 10 + "Maps a button to a channel")
        print("- hardware unmap button (button_id)" + " " * 10 + "Unmaps a button")
        print("- help" + " " * 10 + "Shows this help")
        print("- exit" + " " * 10 + "Exits the program")

    else:
        print("Unknown command")

A.stop_output()

sys.exit("Done")



import json
import sys
import time
import os
import numpy as np

from artnet_output import ArtnetOutputter
from fixture_manager import FixtureManager


class Executer:
    def __init__(self):
        self.FixtureManager = FixtureManager()

    def change_fixture_shutter(self, artnet_outputter: ArtnetOutputter, fixture_id: int, shutter_value: int) -> str:
        # set dmx channel
        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                dmx_patch = self.FixtureManager.calculate_dmx_patch()
                for channel in dmx_patch:
                    if dmx_patch[channel][0] == fixture_id:
                        if dmx_patch[channel][2] == "Shutter":
                            artnet_outputter.change_value_for_channel(channel, shutter_value, False)

        return "Done"

    def change_fixture_dimmer(self, artnet_outputter: ArtnetOutputter, fixture_id, dimmer_value):
        # check if fixture is dimmable
        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)
        dmx_patch = self.FixtureManager.calculate_dmx_patch()
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                for channel in dmx_patch:
                    if dmx_patch[channel][0] == fixture_id:
                        if dmx_patch[channel][2] == "Dimmer":
                            # if fixture has a dimmer channel, use it
                            return self.change_dimmable_fixture_dimmer(artnet_outputter, fixture_id, dimmer_value)

        # seems like fixture is not dimmable, use rgb channels
        return self.change_undimmable_fixture_dimmer(artnet_outputter, fixture_id, dimmer_value)

    def change_dimmable_fixture_dimmer(self, artnet_outputter: ArtnetOutputter, fixture_id, dimmer_value):
        # get dmx channel that is named dimmer
        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                dmx_patch = self.FixtureManager.calculate_dmx_patch()
                for channel in dmx_patch:
                    if dmx_patch[channel][0] == fixture_id:
                        if dmx_patch[channel][2] == "Dimmer":
                            artnet_outputter.change_value_for_channel(channel, dimmer_value, False)

        return "Done"

    def change_undimmable_fixture_dimmer(self, artnet_outputter: ArtnetOutputter, fixture_id, dimmer_value):
        # get rbg channels
        rgb_channels = [0,0,0]
        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                dmx_patch = self.FixtureManager.calculate_dmx_patch()
                for channel in dmx_patch:
                    if dmx_patch[channel][0] == fixture_id:
                        if dmx_patch[channel][2] == "Red":
                            rgb_channels[0] = channel
                        if dmx_patch[channel][2] == "Green":
                            rgb_channels[1] = channel
                        if dmx_patch[channel][2] == "Blue":
                            rgb_channels[2] = channel

        # get old rgb channel values
        with open("internal_files/dmx_output.json") as f:
            data = json.load(f)
        old_rgb_values = [0,0,0]
        old_rgb_values[0] = data[str(rgb_channels[0]).split(".")[0]][str(rgb_channels[0]).split(".")[1]]
        old_rgb_values[1] = data[str(rgb_channels[1]).split(".")[0]][str(rgb_channels[1]).split(".")[1]]
        old_rgb_values[2] = data[str(rgb_channels[2]).split(".")[0]][str(rgb_channels[2]).split(".")[1]]
        # calculate new rgb values
        new_rgb_values = [0,0,0]
        new_rgb_values[0] = round(min(255, 1 + dimmer_value / 255 * old_rgb_values[0]))
        new_rgb_values[1] = round(min(255, 1 + dimmer_value / 255 * old_rgb_values[1]))
        new_rgb_values[2] = round(min(255, 1 + dimmer_value / 255 * old_rgb_values[2]))

        for i in range(len(new_rgb_values)):
            if new_rgb_values[i] == 1:
                new_rgb_values[i] = 0
        # print(new_rgb_values)

        # set dmx channel
        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                dmx_patch = self.FixtureManager.calculate_dmx_patch()
                for channel in dmx_patch:
                    if dmx_patch[channel][0] == fixture_id:
                        if dmx_patch[channel][2] == "Red":
                            artnet_outputter.change_value_for_channel(channel, new_rgb_values[0], True)
                        if dmx_patch[channel][2] == "Green":
                            artnet_outputter.change_value_for_channel(channel, new_rgb_values[1], True)
                        if dmx_patch[channel][2] == "Blue":
                            artnet_outputter.change_value_for_channel(channel, new_rgb_values[2], True)

        return "Done"

    def change_rgb_fixture_color(self, artnet_outputter: ArtnetOutputter, fixture_id, color:list):
        # set dmx channel
        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                dmx_patch = self.FixtureManager.calculate_dmx_patch()
                for channel in dmx_patch:
                    if dmx_patch[channel][0] == fixture_id:
                        if dmx_patch[channel][2] == "Red":
                            artnet_outputter.change_value_for_channel(channel, color[0], False)
                        if dmx_patch[channel][2] == "Green":
                            artnet_outputter.change_value_for_channel(channel, color[1], False)
                        if dmx_patch[channel][2] == "Blue":
                            artnet_outputter.change_value_for_channel(channel, color[2], False)

        return "Done"

    def change_colorwheel_fixture_color(self, artnet_outputter: ArtnetOutputter, fixture_id, input_color):
        # get fixture library id
        fixture_library_id = self.FixtureManager.get_fixture_library_id(fixture_id)

        # get color wheel information from fixture library
        for file in os.listdir("fixtures"):
            mode: dict = {}
            if file.endswith(".json"):
                if file.split("__")[0] == str(fixture_library_id):
                    filepath = os.path.join("fixtures", file)
                    with open(filepath) as f:
                        data = json.load(f)

                    # get color slots
                    color_slots = {}
                    for i in range(len(data["wheels"]["Color Wheel"]["slots"])):
                        slot = data["wheels"]["Color Wheel"]["slots"][i]
                        # print(slot)
                        # print(len(slot))
                        if len(slot) > 1:
                            color_slots[i] = [slot["type"], slot["name"], slot["colors"]]
                        elif len(slot) == 1:
                            color_slots[i] = [slot["type"]]

                    # get dmx slots
                    dmx_slots = {}
                    for i in range(len(data["availableChannels"]["Color"]["capabilities"])):
                        dmx_slot= data["availableChannels"]["Color"]["capabilities"][i]
                        if dmx_slot["type"] == "WheelSlot":
                            if "slotNumber" in dmx_slot:
                                dmx_slots[dmx_slot["slotNumber"] - 1] = dmx_slot["dmxRange"]

                    # combine color_slots and dmx_slots
                    slots = {}
                    for color_slot in color_slots:
                        for dmx_slot in dmx_slots:
                            if color_slot == dmx_slot:
                                if len(color_slots[color_slot]) > 1:
                                    slots[color_slot] = [color_slots[color_slot][0], color_slots[color_slot][1], color_slots[color_slot][2], dmx_slots[dmx_slot]]
                                elif len(color_slots[color_slot]) == 1:
                                    slots[color_slot] = [color_slots[color_slot][0], dmx_slots[dmx_slot]]

        # find best matching color
        slot_colors = []
        for slot in slots:
            if slots[slot][0] == "Open":
                color_rgb= [255, 255, 255]
                slot_colors.append(color_rgb)
            if slots[slot][0] == "Color":
                for color in slots[slot][2]:
                    # convert hex color to rgb
                    h = color.strip('#')
                    color_rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
                    slot_colors.append(color_rgb)
        # caclulate distance between input color and slot colors
        colors = np.array(slot_colors)
        color = np.array(input_color)
        distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
        index_of_smallest = np.where(distances == np.amin(distances))
        smallest_distance = colors[index_of_smallest]
        matching_color_temp = str(smallest_distance).strip("[").strip("]").split(" ")
        matching_color = []
        for el in matching_color_temp:
            if el != "":
                matching_color.append(int(el))
        # find dmx value
        dmx_value = []
        for slot in slots:
            if slots[slot][0] == "Open":
                color_rgb= [255, 255, 255]
                slot_colors.append(color_rgb)
            elif slots[slot][0] == "Color":
                for color in slots[slot][2]:
                    # convert hex color to rgb
                    h = color.strip('#')
                    color_rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
                    slot_colors.append(color_rgb)
            else: break
            # check if the slots color is the matching color
            if matching_color == color_rgb:
                dmx_value = slots[slot][-1][0]
        # check if color was found
        if dmx_value == []:
            return "Color not found"

        #set dmx channel to value
        with open("internal_files/fixture_patch.json") as f:
            data = json.load(f)
        for i in range(len(data)):
            if data[i]["id"] == fixture_id:
                dmx_patch = self.FixtureManager.calculate_dmx_patch()
                for channel in dmx_patch:
                    if dmx_patch[channel][0] == fixture_id:
                        if dmx_patch[channel][2] == "Color":
                            artnet_outputter.change_value_for_channel(channel, dmx_value, False)

        return "Done"


# A = ArtnetOutputter(512)
# A.start_output()
#
# time.sleep(2)
#
# E = Executer()
#
# A.generate_empty_dmx_output_file()

# print(E.change_rgb_fixture_color(A, 1, [100, 255, 25]))
# print(E.change_colorwheel_fixture_color(A, 100, [0, 0, 255]))

# print(E.change_dimmable_fixture_dimmer(A, 100, 255))
# print(E.change_undimmable_fixture_dimmer(A, 1, 255))

# print(E.open_fixture_shutter(A, 100))

# time.sleep(10)
# A.stop_output()
#
# sys.exit("Done")

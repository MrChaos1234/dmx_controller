import json
import sys
import time
import os
import numpy as np
import threading

from py_managers.fixture_manager import FixtureManager


class DmxDataGenerationManager:
    def __init__(self):
        self.fixture_manager = FixtureManager()

    def change_temp_cue_drgbw_fixture_color(self, fixture_id: int, dimmer: int, r: int, g: int, b: int, w: int):
        channel_data = {"1": dimmer, "2": r, "3": g, "4": b, "5": w, "6": 0}
        fixture = {"fixture_id": fixture_id, "channel_data": channel_data}
        
        # ==> fixture = {"fixture_id": 1, "channel_data": {"1":255, "2": 255, "3": 0, "4": 0, "5": 0, "6": 0}}
                
        output = []    
        
        # ==> output = [{"fixture_id": 1, "channel_data": {"1":255, "2": 255, "3": 0, "4": 0, "5": 0, "6": 0}}, {"fixture_id": 2, "channel_data":{"1":255, "2": 255, "3": 0, "4": 0, "5": 0, "6": 0}}]
     
        with open("data/temp_cue_data.json") as f:
            data = json.load(f)

        appended = False
        for in_fixture in data:
            print(in_fixture)
            if in_fixture["fixture_id"] == fixture_id:
                output.append(fixture)
                print("in not")
                appended = True
            else:
                output.append(in_fixture)
                      
        if not appended:
            output.append(fixture)
                        
        with open("data/temp_cue_data.json", "w") as f:
            json.dump(output, f, indent=4, separators=(',', ': '))

        return
    
    def reset_temp_cue_data(self):
        data = []
        with open("data/temp_cue_data.json", "w") as f:
            json.dump(data, f, indent=4, separators=(',', ': '))
        return
        
    def get_temp_cue_data(self):
        with open("data/temp_cue_data.json") as f:
            data = json.load(f)
        return data
            
    ### Active was in a file earlyer. Moved it to a variable for performance reasons #### 
    
    # def add_cue_to_active(self, cue_data):
    #     with open("data/active.json") as f:
    #         data = json.load(f)

    #     for cue in data:
    #         if cue["id"] == cue_data["id"]:
    #             print("Cue is already active")
    #             return

    #     data.append({"id": cue_data["id"],
    #                  "data": cue_data["data"]})

    #     with open("data/active.json", "w") as f:
    #         json.dump(data, f, indent=4, separators=(',', ': '))

    # def zero_cue_in_active(self, cue_data):        
    #     with open("data/active.json") as f:
    #         data = json.load(f)
        
    #     output = []
        
    #     for cue in data:
    #         fixture_data = []
    #         if cue["id"] == cue_data["id"]:
    #             fixture_output = {}
    #             for fixture in cue["data"]:
    #                 channel_data = {}
    #                 for channel in fixture["channel_data"]:
    #                     fixture_output["fixture_id"] = fixture["fixture_id"]
    #                     channel_data[channel] = 0
    #                 fixture_output["channel_data"] = channel_data
    #                 fixture_data.append(fixture_output)
    #                 fixture_output = {}
    #             single_cue = {"id": cue_data["id"],"data": fixture_data}
    #             output.append(single_cue)
                                    
    #     with open("data/active.json", "w") as f:
    #         json.dump(output, f, indent=4, separators=(',', ': '))
        
        
    # def remove_cue_from_active(self, cue_data):
    #     print("remove cue from active")

    #     with open("data/active.json") as f:
    #         data = json.load(f)

    #     for cue in data:
    #         if cue["id"] == cue_data["id"]:
    #             data.remove(cue)

    #     with open("data/active.json", "w") as f:
    #         json.dump(data, f, indent=4, separators=(',', ': '))

    # def clear_active(self):
    #     with open("data/active.json") as f:
    #         data = json.load(f)

    #     data = []

    #     with open("data/active.json", "w") as f:
    #         json.dump(data, f, indent=4, separators=(',', ': '))

    def change_fixture_live_dmx_values(self, fixture_id, values):
        # calculate dmx values and channels for each fixture in each cue 
        fixtures = self.fixture_manager.calculate_fixture_patch()   # get starting adress
        for fixtures_fixture in fixtures:
            if fixtures_fixture["id"] == fixture_id:
                start_adress = fixtures_fixture["dmx_start_address"]
                channels: list = self.list_available_fixtures()[fixtures["fixture_library_id"]][1][fixtures["channel_mode"]][1]
                print("channels: " + str(channels))
            # for i_channel in range(len(channels)):
            #     # [fixture_id, fixture_display_name, channel_name]
            #     build_list = [data[i]["id"], data[i]["display_name"], channels[i_channel]]
            #     dmx_patch[str(int(str(data[i]["dmx_start_address"]).split(".")[1]) + i_channel)] = build_list
    
    
    
    def turn_down_all_channels(self, fixture_id):
        pass
        
        
        
        
        
    # def change_fixture_dimmer(self, fixture_id, dimmer_value):
    #     # check if fixture is dimmable
    #     with open("data/fixture_patch.json") as f:
    #         data = json.load(f)
    #     dmx_patch = self.FixtureManager.calculate_dmx_patch()

    #     output = []

    #     for i in range(len(data)):
    #         if data[i]["id"] == fixture_id:
    #             for channel in dmx_patch:
    #                 if dmx_patch[channel][0] == fixture_id:
    #                     if dmx_patch[channel][2] == "Dimmer":
    #                         # if fixture has a dimmer channel, use it
    #                         output = [channel, dimmer_value]

    #                         for channel in data["0"]:
    #                             for i_output in range(len(output)):
    #                                 if int(output[i_output][0]) == int(channel):
    #                                     data["0"][channel] = output[i_output][1]

    #                         dmx_data = dict(data["0"])

    #                         return dmx_data

    #     # seems like fixture is not dimmable, use rgb channels
    #     print("Fixture is not dimmable")
    #     return

    # def change_undimmable_fixture_dimmer(self, artnet_outputter: ArtnetManager, fixture_id, dimmer_value):
    #     # get rbg channels
    #     rgb_channels = [0,0,0]
    #     with open("internal_files/fixture_patch.json") as f:
    #         data = json.load(f)
    #     for i in range(len(data)):
    #         if data[i]["id"] == fixture_id:
    #             dmx_patch = self.FixtureManager.calculate_dmx_patch()
    #             for channel in dmx_patch:
    #                 if dmx_patch[channel][0] == fixture_id:
    #                     if dmx_patch[channel][2] == "Red":
    #                         rgb_channels[0] = channel
    #                     if dmx_patch[channel][2] == "Green":
    #                         rgb_channels[1] = channel
    #                     if dmx_patch[channel][2] == "Blue":
    #                         rgb_channels[2] = channel

    #     # get old rgb channel values
    #     with open("internal_files/dmx_output.json") as f:
    #         data = json.load(f)
    #     old_rgb_values = [0,0,0]
    #     old_rgb_values[0] = data[str(rgb_channels[0]).split(".")[0]][str(rgb_channels[0]).split(".")[1]]
    #     old_rgb_values[1] = data[str(rgb_channels[1]).split(".")[0]][str(rgb_channels[1]).split(".")[1]]
    #     old_rgb_values[2] = data[str(rgb_channels[2]).split(".")[0]][str(rgb_channels[2]).split(".")[1]]
    #     # calculate new rgb values
    #     new_rgb_values = [0,0,0]
    #     new_rgb_values[0] = round(min(255, 1 + dimmer_value / 255 * old_rgb_values[0]))
    #     new_rgb_values[1] = round(min(255, 1 + dimmer_value / 255 * old_rgb_values[1]))
    #     new_rgb_values[2] = round(min(255, 1 + dimmer_value / 255 * old_rgb_values[2]))

    #     for i in range(len(new_rgb_values)):
    #         if new_rgb_values[i] == 1:
    #             new_rgb_values[i] = 0
    #     # print(new_rgb_values)

    #     # set dmx channel
    #     with open("internal_files/fixture_patch.json") as f:
    #         data = json.load(f)
    #     for i in range(len(data)):
    #         if data[i]["id"] == fixture_id:
    #             dmx_patch = self.FixtureManager.calculate_dmx_patch()
    #             for channel in dmx_patch:
    #                 if dmx_patch[channel][0] == fixture_id:
    #                     if dmx_patch[channel][2] == "Red":
    #                         artnet_outputter.change_value_for_channel(channel, new_rgb_values[0], True)
    #                     if dmx_patch[channel][2] == "Green":
    #                         artnet_outputter.change_value_for_channel(channel, new_rgb_values[1], True)
    #                     if dmx_patch[channel][2] == "Blue":
    #                         artnet_outputter.change_value_for_channel(channel, new_rgb_values[2], True)

    #     return "Done"

    # def change_fixture_shutter(self, artnet_outputter: ArtnetManager, fixture_id: int, shutter_value: int) -> str:
    #     # set dmx channel
    #     with open("internal_files/fixture_patch.json") as f:
    #         data = json.load(f)
    #     for i in range(len(data)):
    #         if data[i]["id"] == fixture_id:
    #             dmx_patch = self.FixtureManager.calculate_dmx_patch()
    #             for channel in dmx_patch:
    #                 if dmx_patch[channel][0] == fixture_id:
    #                     if dmx_patch[channel][2] == "Shutter":
    #                         artnet_outputter.change_value_for_channel(channel, shutter_value, False)

    #     return "Done"

    # def change_colorwheel_fixture_color(self, artnet_outputter: ArtnetManager, fixture_id, input_color):
    #     # get fixture library id
    #     fixture_library_id = self.FixtureManager.get_fixture_library_id(fixture_id)

    #     # get color wheel information from fixture library
    #     for file in os.listdir("fixtures"):
    #         mode: dict = {}
    #         if file.endswith(".json"):
    #             if file.split("__")[0] == str(fixture_library_id):
    #                 filepath = os.path.join("fixtures", file)
    #                 with open(filepath) as f:
    #                     data = json.load(f)

    #                 # get color slots
    #                 color_slots = {}
    #                 for i in range(len(data["wheels"]["Color Wheel"]["slots"])):
    #                     slot = data["wheels"]["Color Wheel"]["slots"][i]
    #                     # print(slot)
    #                     # print(len(slot))
    #                     if len(slot) > 1:
    #                         color_slots[i] = [slot["type"], slot["name"], slot["colors"]]
    #                     elif len(slot) == 1:
    #                         color_slots[i] = [slot["type"]]

    #                 # get dmx slots
    #                 dmx_slots = {}
    #                 for i in range(len(data["availableChannels"]["Color"]["capabilities"])):
    #                     dmx_slot= data["availableChannels"]["Color"]["capabilities"][i]
    #                     if dmx_slot["type"] == "WheelSlot":
    #                         if "slotNumber" in dmx_slot:
    #                             dmx_slots[dmx_slot["slotNumber"] - 1] = dmx_slot["dmxRange"]

    #                 # combine color_slots and dmx_slots
    #                 slots = {}
    #                 for color_slot in color_slots:
    #                     for dmx_slot in dmx_slots:
    #                         if color_slot == dmx_slot:
    #                             if len(color_slots[color_slot]) > 1:
    #                                 slots[color_slot] = [color_slots[color_slot][0], color_slots[color_slot][1], color_slots[color_slot][2], dmx_slots[dmx_slot]]
    #                             elif len(color_slots[color_slot]) == 1:
    #                                 slots[color_slot] = [color_slots[color_slot][0], dmx_slots[dmx_slot]]

    #     # find best matching color
    #     slot_colors = []
    #     for slot in slots:
    #         if slots[slot][0] == "Open":
    #             color_rgb= [255, 255, 255]
    #             slot_colors.append(color_rgb)
    #         if slots[slot][0] == "Color":
    #             for color in slots[slot][2]:
    #                 # convert hex color to rgb
    #                 h = color.strip('#')
    #                 color_rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    #                 slot_colors.append(color_rgb)
    #     # caclulate distance between input color and slot colors
    #     colors = np.array(slot_colors)
    #     color = np.array(input_color)
    #     distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
    #     index_of_smallest = np.where(distances == np.amin(distances))
    #     smallest_distance = colors[index_of_smallest]
    #     matching_color_temp = str(smallest_distance).strip("[").strip("]").split(" ")
    #     matching_color = []
    #     for el in matching_color_temp:
    #         if el != "":
    #             matching_color.append(int(el))
    #     # find dmx value
    #     dmx_value = []
    #     for slot in slots:
    #         if slots[slot][0] == "Open":
    #             color_rgb= [255, 255, 255]
    #             slot_colors.append(color_rgb)
    #         elif slots[slot][0] == "Color":
    #             for color in slots[slot][2]:
    #                 # convert hex color to rgb
    #                 h = color.strip('#')
    #                 color_rgb = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    #                 slot_colors.append(color_rgb)
    #         else: break
    #         # check if the slots color is the matching color
    #         if matching_color == color_rgb:
    #             dmx_value = slots[slot][-1][0]
    #     # check if color was found
    #     if dmx_value == []:
    #         return "Color not found"

    #     #set dmx channel to value
    #     with open("internal_files/fixture_patch.json") as f:
    #         data = json.load(f)
    #     for i in range(len(data)):
    #         if data[i]["id"] == fixture_id:
    #             dmx_patch = self.FixtureManager.calculate_dmx_patch()
    #             for channel in dmx_patch:
    #                 if dmx_patch[channel][0] == fixture_id:
    #                     if dmx_patch[channel][2] == "Color":
    #                         artnet_outputter.change_value_for_channel(channel, dmx_value, False)

    #     return "Done"

    # # map hardware to fixture attributes
    # def start_map_fader_to_channel(self, artnet_outputter: ArtnetManager, pult_hardware_manager: PultHardwareManager, fader_id, channel_id):
    #     self.stop_flag = False
    #     self.map_fader_to_channel_thread = threading.Thread(target=self.map_fader_to_channel, args=(artnet_outputter, pult_hardware_manager, fader_id, channel_id))
    #     self.map_fader_to_channel_thread.start()
    #     return "Done"

    # def map_fader_to_channel(self, artnet_outputter: ArtnetManager, pult_hardware_manager: PultHardwareManager, fader_id, channel_id):
    #     while True:
    #         # get fader value
    #         fader_value = pult_hardware_manager.get_fader_value(fader_id)
    #         # set channel value
    #         artnet_outputter.change_value_for_channel(channel_id, fader_value, True)
    #         if self.stop_flag:
    #             break

    # def stop_map_fader_to_channel(self, fader_id):
    #     self.stop_flag = True
    #     self.map_fader_to_channel_thread.join()
    #     return "Done"

    # def start_map_flash_buttons_to_channels(self, artnet_outputter: ArtnetManager, pult_hardware_manager: PultHardwareManager, starting_channel):
    #     self.stop_flag_1 = False
    #     self.map_flash_buttons_thread = threading.Thread(target=self.map_flash_buttons_to_channels, args=(artnet_outputter, pult_hardware_manager, starting_channel,))
    #     self.map_flash_buttons_thread.start()
    #     return "Done"

    # def map_flash_buttons_to_channels(self, artnet_outputter: ArtnetManager, pult_hardware_manager: PultHardwareManager, starting_channel):
    #     while True:
    #         # get button values
    #         button_values = []
    #         for i in range(1, 4, 1):
    #             button_values.append(pult_hardware_manager.get_button_value(i))

    #         # set channel values
    #         for i in range(len(button_values)):
    #             if button_values[i] == 1:
    #                 artnet_outputter.change_value_for_channel(str(starting_channel).split(".")[0] + "." + str((int(str(starting_channel).split(".")[1]) + i)), str(255), True)
    #             else:
    #                 artnet_outputter.change_value_for_channel(str(starting_channel).split(".")[0] + "." + str((int(str(starting_channel).split(".")[1]) + i)), str(0), True)
    #         if self.stop_flag_1:
    #             break

    # def stop_map_flash_buttons_to_channels(self, button_id):
    #     self.stop_flag_1 = True
    #     self.map_flash_buttons_thread.join()
    #     return "Done"

#
# A = ArtnetManager(512)
# A.start_output()
#
# time.sleep(2)
#
# E = Executer()
# P = PultHardwareManager()
#
# A.generate_empty_dmx_output_file()

# print(E.change_rgb_fixture_color(A, 1, [100, 255, 25]))
# print(E.change_colorwheel_fixture_color(A, 100, [0, 0, 255]))

# print(E.change_dimmable_fixture_dimmer(A, 100, 255))
# print(E.change_undimmable_fixture_dimmer(A, 1, 255))

# print(E.open_fixture_shutter(A, 100))

# E.map_fader_to_channel_thread(A, P, 1, "0.1")


# time.sleep(10)
# A.stop_output()
#
# sys.exit("Done")
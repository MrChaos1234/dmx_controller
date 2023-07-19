from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from py_managers.artnet_manager import ArtnetManager
from py_managers.cue_manager import CueManager
from py_managers.dmx_data_generation_manager import DmxDataGenerationManager
from py_managers.fixture_manager import FixtureManager

import time

class ArtnetOutput(QObject):
    _cue_manager: CueManager
    
    stop_effect_requested = pyqtSignal(int)
       
    def __init__(self, artnet_manager: ArtnetManager, cue_manager: CueManager, dmx_data_generation_manager: DmxDataGenerationManager, parent: QObject = None,):
        super().__init__(parent)
        self._artnet_manager = artnet_manager
        self._cue_manager = cue_manager
        self._dmx_data_generation_manager = dmx_data_generation_manager
        
        self.active_fixtures = [] # replacement for the file! -> this should be faster
        self.active_fixtures2 = [] 
        
        self.cue_data = []
        
        self._fixture_manager: FixtureManager = FixtureManager()
        
        self._all_fixtures = []
        self.fader_cue_realtion = []
        
        self.fader_cue_relation = []
        
    def setup(self) -> None:
        self.update_cue_list()
        self._all_fixtures = self._fixture_manager.calculate_fixture_patch()
        self.fader_cue_realtion = self._cue_manager.get_fader_cue_relation()
        self._artnet_manager.start_output()
        

    @pyqtSlot()
    def update_cue_list(self):
        self.cue_data = self._cue_manager.get_cues()    
        self._all_fixtures = self._fixture_manager.calculate_fixture_patch()
        self.fader_cue_realtion = self._cue_manager.get_fader_cue_relation()
    
    @pyqtSlot()
    def clear_output_handler(self):
        self.update_cue_list()
        self.fader_cue_realtion = self._cue_manager.get_fader_cue_relation()
        ## clear button triggers this function! ##
        pass
        
    @pyqtSlot(int)
    def execute_cue_handler(self, cue_index):
        if cue_index == 0:
            print("no cue selected")
            return
        
        for cue in self.cue_data:
            if cue["id"] == cue_index:
                desired_cue = cue
       
        self.add_cue_to_output_button(desired_cue)
       
    @pyqtSlot(int)
    def clear_cue_handler(self, cue_index):
        if cue_index == 0:
            print("no cue selected")
            return
        for cue in self.cue_data:
            if cue["id"] == cue_index:
                desired_cue = cue
        
        self.subtract_cue_from_output(desired_cue)
      
    @pyqtSlot(int, int)
    def change_dimmer_channel_handler(self, cue_index, fader_value):                
        if cue_index == 0 or cue_index == "None":
            print("no cue selected")
            return
    
        for cue in self.cue_data:
            if cue["id"] == cue_index:
                desired_cue = cue

        self.add_cue_to_output_dimmer_fader(desired_cue, fader_value)
            
    @pyqtSlot(int, int)
    def change_color_red_channel_handler(self, cue_index, fader_value):
        if cue_index == 0 or cue_index == "None":
            print("no cue selected")
            return
    
        for cue in self.cue_data:
            if cue["id"] == cue_index:
                desired_cue = cue

        self.add_cue_to_output_color_red_fader(desired_cue, fader_value)
    
    @pyqtSlot(int, int)
    def change_color_green_channel_handler(self, cue_index, fader_value):
        if cue_index == 0 or cue_index == "None":
            print("no cue selected")
            return
    
        for cue in self.cue_data:
            if cue["id"] == cue_index:
                desired_cue = cue

        self.add_cue_to_output_color_green_fader(desired_cue, fader_value)
    
    @pyqtSlot(int, int)
    def change_color_blue_channel_handler(self, cue_index, fader_value):
        if cue_index == 0 or cue_index == "None":
            print("no cue selected")
            return
    
        for cue in self.cue_data:
            if cue["id"] == cue_index:
                desired_cue = cue

        self.add_cue_to_output_color_blue_fader(desired_cue, fader_value)
        

    def add_cue_to_output_dimmer_fader(self, cue, fader_value):
        # Add Cue to Output:
        # cue = {"id": 1, "cue_name": "Even", "cue_group": 1, "data": [{"fixture_id": 1, "channel_data": {"1:" 0, "2": 255, "3": 0}}, {"fixture_id": 2, "channel_data": {"1:" 0, "2": 255, "3": 0}}]}
        
        output = self._artnet_manager.output_old.copy()
        value_is_255 = False
        value_is_0 = False
        # process the fixtures that are in the active_cues with additive mixing
        for fixture in cue["data"]:
            # calculate dmx values and channels for each fixture in each cue
            for global_fixture in self._all_fixtures:
                if global_fixture["id"] == fixture["fixture_id"]:
                    start_adress = global_fixture["dmx_start_address"]
                    i = 0
                    for rel_channel, value in fixture["channel_data"].items():
                        abs_channel = int(start_adress.split(".")[-1]) + int(rel_channel) - 1
                        # assuming that the dimmer channel is the first channel
                        if i == 0:          
                            value = int(fader_value)# + int(output[int(abs_channel)-1])
                            if value > 255:
                                value = 255
                            output[int(abs_channel)-1] = value
                            if value == 255:
                                value_is_255 = True 
                            if value == 2:
                                value_is_0 = True
                        i += 1
                    
                    break
        
         # if the value is 255 or 0, send it multiple times to make sure it is received
        if value_is_255 or value_is_0:
            for i in range(0, 6):
                self._artnet_manager.output = output
                time.sleep(0.005)
            
        else:
            self._artnet_manager.output = output
        
        
    def add_cue_to_output_color_red_fader(self, cue, fader_value):
        # Add Cue to Output:
        # cue = {"id": 1, "cue_name": "Even", "cue_group": 1, "data": [{"fixture_id": 1, "channel_data": {"1:" 0, "2": 255, "3": 0}}, {"fixture_id": 2, "channel_data": {"1:" 0, "2": 255, "3": 0}}]}

        output = self._artnet_manager.output_old.copy()
        value_is_255 = False
        value_is_0 = False
        # process the fixtures that are in the active_cues with additive mixing
        for fixture in cue["data"]:
            # calculate dmx values and channels for each fixture in each cue
            for global_fixture in self._all_fixtures:
                if global_fixture["id"] == fixture["fixture_id"]:
                    start_adress = global_fixture["dmx_start_address"]
                    i = 0
                    for rel_channel, value in fixture["channel_data"].items():
                        abs_channel = int(start_adress.split(".")[-1]) + int(rel_channel) - 1
                        if i == 1:
                            value = int(fader_value)
                            output[int(abs_channel)-1] = value
                            if value == 255:
                                value_is_255 = True 
                            if value == 0:
                                value_is_0 = True
                        i += 1
                    
                    break
                
        # if the value is 255 or 0, send it multiple times to make sure it is received
        if value_is_255 or value_is_0:
            for i in range(0, 6):
                self._artnet_manager.output = output
                time.sleep(0.005)
            
        else:
            self._artnet_manager.output = output
        
    def add_cue_to_output_color_green_fader(self, cue, fader_value):
        # Add Cue to Output:
        # cue = {"id": 1, "cue_name": "Even", "cue_group": 1, "data": [{"fixture_id": 1, "channel_data": {"1:" 0, "2": 255, "3": 0}}, {"fixture_id": 2, "channel_data": {"1:" 0, "2": 255, "3": 0}}]}
        
        output = self._artnet_manager.output_old.copy()
        value_is_255 = False
        value_is_0 = False
        # process the fixtures that are in the active_cues with additive mixing
        for fixture in cue["data"]:
            # calculate dmx values and channels for each fixture in each cue
            for global_fixture in self._all_fixtures:
                if global_fixture["id"] == fixture["fixture_id"]:
                    start_adress = global_fixture["dmx_start_address"]
                    i = 0
                    for rel_channel, value in fixture["channel_data"].items():
                        abs_channel = int(start_adress.split(".")[-1]) + int(rel_channel) - 1
                        if i == 2:
                            value = int(fader_value)
                            output[int(abs_channel)-1] = value
                            if value == 255:
                                value_is_255 = True 
                            if value == 0:
                                value_is_0 = True
                        i += 1
                    
                    break
        
         # if the value is 255 or 0, send it multiple times to make sure it is received
        if value_is_255 or value_is_0:
            for i in range(0, 6):
                self._artnet_manager.output = output
                time.sleep(0.005)
            
        else:
            self._artnet_manager.output = output
        
    def add_cue_to_output_color_blue_fader(self, cue, fader_value):
        # Add Cue to Output:
        # cue = {"id": 1, "cue_name": "Even", "cue_group": 1, "data": [{"fixture_id": 1, "channel_data": {"1:" 0, "2": 255, "3": 0}}, {"fixture_id": 2, "channel_data": {"1:" 0, "2": 255, "3": 0}}]}
        
        output = self._artnet_manager.output_old.copy()
        value_is_255 = False
        value_is_0 = False
        # process the fixtures that are in the active_cues with additive mixing
        for fixture in cue["data"]:
            # calculate dmx values and channels for each fixture in each cue
            for global_fixture in self._all_fixtures:
                if global_fixture["id"] == fixture["fixture_id"]:
                    start_adress = global_fixture["dmx_start_address"]
                    i = 0
                    for rel_channel, value in fixture["channel_data"].items():
                        abs_channel = int(start_adress.split(".")[-1]) + int(rel_channel) - 1
                        value = int(value)
                        if i == 3:
                            value = int(fader_value)
                            output[int(abs_channel)-1] = value
                            if value == 255:
                                value_is_255 = True 
                            if value == 0:
                                value_is_0 = True
                        i += 1
                    
                    break
        
        # if the value is 255 or 0, send it multiple times to make sure it is received
        if value_is_255 or value_is_0:
            for i in range(0, 6):
                self._artnet_manager.output = output
                time.sleep(0.005)
            
        else:
            self._artnet_manager.output = output
        
    def add_cue_to_output_button(self, cue):
        # Add Cue to Output:
        # cue = {"id": 1, "cue_name": "Even", "cue_group": 1, "data": [{"fixture_id": 1, "channel_data": {"1:" 0, "2": 255, "3": 0}}, {"fixture_id": 2, "channel_data": {"1:" 0, "2": 255, "3": 0}}]}
        
        output = self._artnet_manager.output_old.copy()

        # process the fixtures that are in the active_cues with additive mixing
        for fixture in cue["data"]:
            # calculate dmx values and channels for each fixture in each cue
            for global_fixture in self._all_fixtures:
                if global_fixture["id"] == fixture["fixture_id"]:
                    start_adress = global_fixture["dmx_start_address"]
                    i = 0
                    for rel_channel, value in fixture["channel_data"].items():
                        abs_channel = int(start_adress.split(".")[-1]) + int(rel_channel) - 1
                        value = int(value) #+ int(output[int(abs_channel)-1])  
                        output[int(abs_channel)-1] = value
                        i += 1
                    break
        
        self._artnet_manager.output = output
        
    def add_cue_to_output_effect(self, cue):
        # Add Cue to Output:
        # cue = {"id": 1, "cue_name": "Even", "cue_group": 1, "data": [{"fixture_id": 1, "channel_data": {"1:" 0, "2": 255, "3": 0}}, {"fixture_id": 2, "channel_data": {"1:" 0, "2": 255, "3": 0}}]}
        
        output = self._artnet_manager.output_old.copy()

        # process the fixtures that are in the active_cues with additive mixing
        for fixture in cue["data"]:
            # calculate dmx values and channels for each fixture in each cue
            for global_fixture in self._all_fixtures:
                if global_fixture["id"] == fixture["fixture_id"]:
                    start_adress = global_fixture["dmx_start_address"]
                    i = 0
                    for rel_channel, value in fixture["channel_data"].items():
                        abs_channel = int(start_adress.split(".")[-1]) + int(rel_channel) - 1
                        value = int(value) #+ int(output[int(abs_channel)-1])
                        if value > 255:
                            value = 255
                        output[int(abs_channel)-1] = value

                    break
        
        self._artnet_manager.output = output
    
    def subtract_cue_from_output(self, cue):
        # Zero Cue in new output        
        output = self._artnet_manager.output_old.copy()
        
        # process the fixtures that are in the active_cues with additive mixing
        for fixture in cue["data"]:
            # calculate dmx values and channels for each fixture in each cue
            for global_fixture in self._all_fixtures:
                if global_fixture["id"] == fixture["fixture_id"]:
                    start_adress = global_fixture["dmx_start_address"]
                    for rel_channel, value in fixture["channel_data"].items():
                        abs_channel = int(start_adress.split(".")[-1]) + int(rel_channel) - 1
                        new_value = 0
                        output[int(abs_channel)-1] = new_value
                                            
                    break
                
        self._artnet_manager.output = output    


    ## verlegt direkt in effects manager, damit es da in thread laufen kann
    
    # def add_cue_to_output_fade(self, cue, fade_time):
    #     # Add Cue to Output:
    #     # cue = {"id": 1, "cue_name": "Even", "cue_group": 1, "data": [{"fixture_id": 1, "channel_data": {"1:" 0, "2": 255, "3": 0}}, {"fixture_id": 2, "channel_data": {"1:" 0, "2": 255, "3": 0}}]}
       
    #     fade = round(fade_time * 30)
    #     for passes in range(0, fade):
    #         self._artnet_manager.done = False
    #         output = self._artnet_manager.output_old.copy()
    #         # wait for the sende to finish
    #         # process the fixtures that are in the active_cues with additive mixing
    #         for fixture in cue["data"]:
    #             # calculate dmx values and channels for each fixture in each cue
    #             for global_fixture in self._all_fixtures:
    #                 if global_fixture["id"] == fixture["fixture_id"]:
    #                     start_adress = global_fixture["dmx_start_address"]
    #                     for rel_channel, value in fixture["channel_data"].items():
    #                         i = 0
    #                         abs_channel = int(start_adress.split(".")[-1]) + int(rel_channel) - 1
                            
    #                         if value != 0:
    #                             new_value = round(int(value) / fade) * passes + 1
    #                         else:
    #                             new_value = 0
                                
    #                         if new_value > 255:
    #                             new_value = 255

    #                         output[int(abs_channel)-1] = new_value
    #                         i = i + 1
                    
    #                     break
    #         #print("new: " + str(output) + "\n")
    #         #print("old: " + str(self._artnet_manager.output_old) + "\n")
            
    #         self._artnet_manager.output = output
            
    #         while not self._artnet_manager.done:
    #             #print("waiting")
    #             pass
            
    ## ende 
        
        
      
       
       
    
    ## old ##
    ### handling of active_cues ### 
     
    # def add_cue_to_active(self, cue):
    #     # Add Cue to Active:
    #     # cue = {"id": 1, "cue_name": "Even", "cue_group": 1, "data": [{"fixture_id": 1, "channel_data": {"1:" 0, "2": 255, "3": 0}}, {"fixture_id": 2, "channel_data": {"1:" 0, "2": 255, "3": 0}}]}
    #     output = []
    #     if len(self.active_fixtures2) == 0:
    #         # if there are no active fixtures, we can just add the cue to the active fixtures
    #         for fixture in cue["data"]:
    #             output.append(fixture)            
    #     else:
    #         # check which fixtures are already in the active_cues
    #         fixtures_in_active = []
    #         for active_fixture in self.active_fixtures2:
    #             output_fixture = {}
    #             for fixture in cue["data"]:
    #                 if active_fixture["fixture_id"] == fixture["fixture_id"]:
    #                     fixtures_in_active.append(fixture["fixture_id"])
                    
    #         # calculate which fixtures are not in the active_cues
    #         fixtures_not_in_active = [fixture["fixture_id"] for fixture in cue["data"] if fixture["fixture_id"] not in fixtures_in_active]
    
    #         # process the fixtures that are in the active_cues with additive mixing
    #         for active_fixture in self.active_fixtures2:
    #             output_fixture = {}
    #             for fixture in cue["data"]:
    #                 if active_fixture["fixture_id"] == fixture["fixture_id"]:
    #                     # add values and add to output
    #                     channel_data = {}
    #                     for channel in fixture["channel_data"]:
    #                         value = active_fixture["channel_data"][channel] + fixture["channel_data"][channel]
    #                         if value > 255:
    #                             value = 255
    #                         channel_data[channel] = value
    #                     output_fixture["fixture_id"] = fixture["fixture_id"]
    #                     output_fixture["channel_data"] = channel_data        
    #                     output.append(output_fixture)
    #                     output_fixture = {}
    #                     break
                        
    #         # process the fixtures that are not in the active_cues with just adding them to the output
    #         fixtures_in_cue = cue["data"]
    #         for fixture in fixtures_in_cue:
    #             if fixture["fixture_id"] in fixtures_not_in_active:
    #                 output.append(fixture)

            
    #     self.active_fixtures2 = output
    #     #print(self.active_fixtures)
    #     self._artnet_manager.artnet_manager_active_fixtures2_copy = self.active_fixtures2
           
                                        
    # def subtract_cue_to_active(self, cue):
    #     # Zero Cue in new Active        
    #     output = []
    #     for active_fixture in self.active_fixtures2:
    #             output_fixture = {}
    #             for fixture in cue["data"]:
    #                 if active_fixture["fixture_id"] == fixture["fixture_id"]:
    #                     # if the fixture is already in the active_cues, we have to add the channel data to the existing channel data
    #                     #print("have to shut down:" + str(fixture["fixture_id"]))
    #                     channel_data = {}
    #                     for channel in fixture["channel_data"]:
    #                         value = active_fixture["channel_data"][channel] - fixture["channel_data"][channel]
    #                         if value < 0:
    #                             value = 0
    #                         channel_data[channel] = value
    #                     output_fixture["fixture_id"] = fixture["fixture_id"]
    #                     output_fixture["channel_data"] = channel_data  
    #                     #print(output_fixture)      
    #                     output.append(output_fixture)
    #                     output_fixture = {}
    #                     break
        
    #     self.active_fixtures2 = output
    #     #print(self.active_fixtures)
    #     self._artnet_manager.artnet_manager_active_fixtures2_copy = self.active_fixtures2
    
    # only for effect -> adds cues absolute -> no mixing 
    def add_cue_to_active_effect_only(self, cue):
        # Add Cue to Active:
        # cue = {"id": 1, "cue_name": "Even", "cue_group": 1, "data": [{"fixture_id": 1, "channel_data": {"1:" 0, "2": 255, "3": 0}}, {"fixture_id": 2, "channel_data": {"1:" 0, "2": 255, "3": 0}}]}
        output = []
        if len(self.active_fixtures) == 0:
            # if there are no active fixtures, we can just add the cue to the active fixtures
            for fixture in cue["data"]:
                output.append(fixture)            
        else:
            # check which fixtures are already in the active_cues
            fixtures_in_active = []
            for active_fixture in self.active_fixtures:
                output_fixture = {}
                for fixture in cue["data"]:
                    if active_fixture["fixture_id"] == fixture["fixture_id"]:
                        fixtures_in_active.append(fixture["fixture_id"])
                    
            # calculate which fixtures are not in the active_cues
            fixtures_not_in_active = [fixture["fixture_id"] for fixture in cue["data"] if fixture["fixture_id"] not in fixtures_in_active]
    
            # process the fixtures that are in the active_cues with additive mixing
            for active_fixture in self.active_fixtures:
                output_fixture = {}
                for fixture in cue["data"]:
                    if active_fixture["fixture_id"] == fixture["fixture_id"]:
                        channel_data = {}
                        for channel in fixture["channel_data"]:
                            value = fixture["channel_data"][channel]
                            channel_data[channel] = value
                        output_fixture["fixture_id"] = fixture["fixture_id"]
                        output_fixture["channel_data"] = channel_data        
                        output.append(output_fixture)
                        output_fixture = {}
                        break
                        
            # process the fixtures that are not in the active_cues with just adding them to the output
            fixtures_in_cue = cue["data"]
            for fixture in fixtures_in_cue:
                if fixture["fixture_id"] in fixtures_not_in_active:
                    output.append(fixture)

            
        self.active_fixtures = output
        #print(self.active_fixtures)
        self._artnet_manager.artnet_manager_active_fixtures_copy = self.active_fixtures
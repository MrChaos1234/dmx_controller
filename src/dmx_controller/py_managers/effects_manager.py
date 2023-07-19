import json
import sys
import time
import os
import numpy as np
import threading

from py_managers.fixture_manager import FixtureManager
from py_managers.cue_manager import CueManager
from py_managers.dmx_data_generation_manager import DmxDataGenerationManager
from py_managers.artnet_manager import ArtnetManager
from py_components.artnet_output import ArtnetOutput
from py_managers.cue_manager import CueManager
from py_managers.fixture_manager import FixtureManager

class EffectsManager():
    def __init__(self, artnet_manager: ArtnetManager, artnet_output: ArtnetOutput):
        self.fixture_manager = FixtureManager()
        self.cue_manager = CueManager()
        self.dmx_data_generation_manager = DmxDataGenerationManager()
        self._artnet_manager = artnet_manager
        self._artnet_output = artnet_output
        self.effect_speed: list = [2, 2, 2, 2]
        self.effect_fade: list = [0, 0, 0, 0]
        self.cue_manager = CueManager()
        self._fixture_manager = FixtureManager()

        self.effect_stop: bool = False
        self.effect_cues: list = []
        self.effect_running: bool = False
        self.fade_running: bool = False
        
        self._all_fixtures = self._fixture_manager.calculate_fixture_patch()

        # self.dmx_data_generation_manager.clear_active()

    def set_effect_speed(self, effect_id, speed):
        #print("effect speed: " + str(speed))
        self.effect_speed[effect_id-1] = speed

    
    def set_effect_fade(self, effect_id, fade):
        #print("effect fade: " + str(fade))
        self.effect_fade[effect_id-1] = fade
    
    def run_effect(self, effect_id: int):
        if self.effect_running:
            print("effect already running")
            return
        self.effect_running = True
        with open("data/effects.json") as f:
            data = json.load(f)

        for effect in data:
            if effect["id"] == effect_id:
                self.effect_cues = effect["cues"]
                #print(self.effect_1_cues)
                self.output_thread = threading.Thread(target=self.effect_thread_1, name="Effect 1")
                self.output_thread.start()

    def stop_effect(self, effect_id: int):
        # clear output -> first set output again to high, then to 0 and then remove from active
        cue_data = self.cue_manager.get_cues()
        for cue in cue_data:
            if cue["id"] in self.effect_cues:
                self._artnet_output.subtract_cue_from_output(cue)
              
        # stop thread
        self.effect_stop = True
        self.output_thread.join()
        self.effect_stop = False
        
        self.effect_running = False

    def set_effect_cues(self, effect_id: int, cues: list):
        with open("data/effects.json") as f:
            data = json.load(f)
        
        for effect in data:
            if effect["id"] == effect_id:
                effect["cues"] = cues
        
        with open("data/effects.json", "w") as f:
            json.dump(data, f, indent=4)
    
    def get_effect_cues(self):
        with open("data/effects.json") as f:
            data = json.load(f)
            
        output = []
        
        for effect in data:
            output.append(effect["cues"])
            
        return output
            

    # Threads
    def effect_thread_1(self):
        data = []
        cue_data = self.cue_manager.get_cues()
        for cue in cue_data:
            if cue["id"] in self.effect_cues:
                data.append(cue)
                
        while not self.effect_stop:
            for cue in data:     
                if self.effect_fade[0] > 0: ### -> Problem noch: während des Fades geht nichts anderes mehr
                                            ### das ist komisch, weil eigentlich sind wir hier ja in nem thread
                                            ### warscheinlich wegen dem Output file. das wird hier so oft verändert dass 
                                            ### die anderen äderungen nicht wahr werden können
                    # Add Cue to Output:
                    # cue = {"id": 1, "cue_name": "Even", "cue_group": 1, "data": [{"fixture_id": 1, "channel_data": {"1:" 0, "2": 255, "3": 0}}, {"fixture_id": 2, "channel_data": {"1:" 0, "2": 255, "3": 0}}]}
                    fade_time = self.effect_fade[0]
                    fade = round(fade_time * 30)
                    for passes in range(0, fade):
                        self._artnet_manager.done = False
                        output = self._artnet_manager.output_old.copy()
                        # wait for the sende to finish
                        # process the fixtures that are in the active_cues with additive mixing
                        for fixture in cue["data"]:
                            # calculate dmx values and channels for each fixture in each cue
                            for global_fixture in self._all_fixtures:
                                if global_fixture["id"] == fixture["fixture_id"]:
                                    start_adress = global_fixture["dmx_start_address"]
                                    i = 0
                                    for rel_channel, value in fixture["channel_data"].items():
                                        abs_channel = int(start_adress.split(".")[-1]) + int(rel_channel) - 1
                                        if value != 0:
                                            new_value = round(int(value) / fade) * passes + 1
                                        else:
                                            new_value = 0
                                                
                                        if new_value > 255:
                                            new_value = 255
                                        output[int(abs_channel)-1] = new_value
                                            
                                        i+= 1

                                    break
                        #print("new: " + str(output) + "\n")
                        #print("old: " + str(self._artnet_manager.output_old) + "\n")
                        
                        self._artnet_manager.output = output
                        
                        while not self._artnet_manager.done:
                            #print("waiting" + str(wait))
                            #print(self._artnet_manager.done)
                            time.sleep(0.01)
                    
                    
                else:
                    self._artnet_output.add_cue_to_output_effect(cue)
                
                if self.effect_stop:
                    break
                time.sleep(self.effect_speed[0])
                
                if self.fade_running:
                    pass
                
                if self.effect_stop:
                    break
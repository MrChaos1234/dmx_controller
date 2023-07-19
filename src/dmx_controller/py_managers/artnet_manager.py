from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QThread
from stupidArtnet import StupidArtnet, StupidArtnetServer
import random
import time
import threading
import json

from py_managers.dmx_data_generation_manager import DmxDataGenerationManager
from py_managers.fixture_manager import FixtureManager


class ArtnetManager(QObject):
    
    sending_done: pyqtSignal = pyqtSignal()
    
    def __init__(self, packet_size: int, parent: QObject = None):
        super().__init__(parent)
        self.a = StupidArtnet()
        self.packet_size = packet_size
        self.output_thread = threading.Thread()
        self.dmx_queue = [[1, 0]]
        self.stop = False
        self.update_artnet_out = False
        self.update_artnet_out2 = False
        self._dmx_data_generation_manager = DmxDataGenerationManager()
        self._fixture_manager = FixtureManager()
        self.artnet_manager_active_fixtures_copy = []
        self.artnet_manager_active_fixtures2_copy = []
        
        self.output = []
        self.output_old = []
        
        self.done = False
        
        for i in range(512):  # fill the output lists with 0
            self.output.append(0)
            self.output_old.append(0)

    def start_output(self) -> None:
        
        self.sending_done.connect(self.sending_done_handler)
        
        target_ip = "255.255.255.255"
        packet_size = self.packet_size  # only even numbers are working
        universe = 0
        self.a = StupidArtnet(target_ip, universe, packet_size, 40, True, True)
        self.a.set_simplified(False)
        self.a.set_net(0)
        self.a.set_subnet(0)
        print(self.a)  # print the init log of StupidArtnet
        self.a.start()

        self.output_thread = QThread()
        
        self.output_thread = threading.Thread(target=self.output_active_thread, name="Outputter")
        self.output_thread.start()
        
        self.update_artnet_out = True

    def stop_output(self):
        self.a.blackout()
        self.a.stop()
        self.stop = True
        self.output_thread.join()

    @pyqtSlot()
    def sending_done_handler(self):
        print("sending done")
        self.done = True
        
    def output_active_thread(self):
        while True:
            if self.output != self.output_old:
                self.done = False
                # if output changed, update artnet output
                #print("output changed - update artnet output")
                data = self.output
                output_packet = bytearray(self.packet_size)
                for i in range(self.packet_size):
                    output_packet[i] = self.output_old[i]
                
                for channel in range(0, 512):
                    if data[channel] != self.output_old[channel]:
                        #print("diff at channel " + str(channel + 1) + " - new value: " + str(data[channel]))
                        output_packet[channel] = data[channel]
                
                self.a.set(output_packet)
                # at the end , copy the current output to the old output
                self.output_old = data
                      
                # print("artnet_output updated")
                
                self.done = True
                #self.sending_done.emit()
                
                time.sleep(0.0015) # max 40 packets per second -> 0.025 seconds per packet
                
            time.sleep(0.025) # max 40 packets per second -> 0.025 seconds per packet
            
            if self.stop:
                break
    

    ### sicherheitskopie vom alten prinzip
    
    # def output_active_thread(self):
    #     # take everything in active.json and write it to the output
    #     while True:
    #         if self.update_artnet_out:                
    #             # with open("data/active.json") as f:
    #             #     data = json.load(f)
    #             data = self.artnet_manager_active_fixtures_copy
    #             for fixture in data:
    #                 # calculate dmx values and channels for each fixture in each cue
    #                 fixtures = self._fixture_manager.calculate_fixture_patch()   # get starting adress
    #                 for fixtures_fixture in fixtures:
    #                     if fixtures_fixture["id"] == fixture["fixture_id"]:
    #                         start_adress = fixtures_fixture["dmx_start_address"]

    #                 for rel_channel, value in fixture["channel_data"].items():
    #                     i = 0
    #                     abs_channel = int(start_adress.split(".")[-1]) + int(rel_channel) - 1
    #                     wished_value = int(value)
                        
    #                     # if value from somewhere else is higher, use this value
    #                     # ?? hm doof
                        
    #                     self.a.set_single_value(int(abs_channel), int(value))
    #                     i = i + 1
                    
    #         #print("updated artnet output") 
    #         self.update_artnet_out = False     
            
            
    #         if self.update_artnet_out2:
    #             data = self.artnet_manager_active_fixtures2_copy
    #             for fixture in data:
    #                 # calculate dmx values and channels for each fixture in each cue
    #                 fixtures = self._fixture_manager.calculate_fixture_patch()   # get starting adress
    #                 for fixtures_fixture in fixtures:
    #                     if fixtures_fixture["id"] == fixture["fixture_id"]:
    #                         start_adress = fixtures_fixture["dmx_start_address"]

    #                 for rel_channel, value in fixture["channel_data"].items():
    #                     i = 0
    #                     abs_channel = int(start_adress.split(".")[-1]) + int(rel_channel) - 1
    #                     self.a.set_single_value(int(abs_channel), int(value))
    #                     i = i + 1    
            
    #         self.update_artnet_out2 = False
            
    #         if self.stop:
    #             break
            
    #         time.sleep(0.03)
    
    # def set_single_channel(self, channel, value):
    #     self.a.set_single_value(channel, value)         
                
                
    ### ende
    
    
    # def build_output_package(self):
    #     packet = bytearray(self.packet_size)
    #     packet_old = bytearray(self.packet_size)

    #     for x in range(self.packet_size):
    #         packet[x] = 0
    #         packet_old[x] = 0

    #     while True:
    #         if len(self.dmx_queue) > 0:
    #             # print(self.dmx_queue)
    #             packet[int(self.dmx_queue[0][0])-1] = int(self.dmx_queue[0][1])
    #             self.dmx_queue.pop(0)
    #         else:
    #             packet = packet_old
    #         self.a.set(packet)
    #         # print(self.dmx_queue)
    #         time.sleep(0.03)
    #         packet_old = packet
    #         if self.stop:
    #             break

    # def change_value_for_channel(self, channel_raw: str, value, temp: bool):
    #     universe, channel = str(channel_raw).split(".")
    #     dmx_value = [channel, value]
    #     print(dmx_value)
    #     self.dmx_queue.append(dmx_value)

    #     t = time.time()
    #     if not temp:
    #         # change value in the dmx_output file
    #         # read file
    #         with open("data/dmx_output.json") as f:
    #             data = json.load(f)

    #         # change value for desired channel
    #         data[universe][channel] = int(value)

    #         # safe to file again
    #         with open("data/dmx_output.json", "w") as f:
    #             json.dump(data, f, indent=4, separators=(',', ': '))

    #     ti = time.time()
    #     print("Time wirte json" + str(ti-t))


    # def generate_empty_dmx_output_file(self):
    #     data = {}
    #     empty_universe = {}
    #     for channel in range(1, 513, 1):
    #         empty_universe[str(channel)] = 255

    #     for universe in range(3):
    #         data[universe] = empty_universe

    #     with open("data/dmx_output.json", "w") as f:
    #         json.dump(data, f, indent=4, separators=(',', ': '))


# A = ArtnetManager(512)
# A.start_output()
# input("Press Enter to start output")
# A.generate_empty_dmx_output_file()

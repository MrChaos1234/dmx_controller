from stupidArtnet import StupidArtnet, StupidArtnetServer
import random
import time
import threading
import json


class ArtnetManager:
    def __init__(self, packet_size):
        pass

    def start_output(self) -> None:
        self.packet_size = 512
        self.stop = False
        self.a = StupidArtnet()
        target_ip = "255.255.255.255"
        packet_size = self.packet_size # only even numbers are working
        universe = 0
        self.a = StupidArtnet(target_ip, universe, packet_size, 40, True, True)
        self.a.set_simplified(False)
        self.a.set_net(0)
        self.a.set_subnet(0)
        print(self.a)  # print the init log of StupidArtnet
        self.a.start()

        self.output_thread = threading.Thread()
        self.dmx_queue = [[1, 0]]

        self.output_thread = threading.Thread(target=self.build_output_package, name="Outputter")
        self.output_thread.start()

    def stop_output(self):
        self.a.blackout()
        self.a.stop()
        self.stop = True
        self.output_thread.join()

    def build_output_package(self):
        packet = bytearray(self.packet_size)
        packet_old = bytearray(self.packet_size)

        for x in range(self.packet_size):
            packet[x] = 0
            packet_old[x] = 0

        while True:
            if len(self.dmx_queue) > 0:
                # print(self.dmx_queue)
                packet[int(self.dmx_queue[0][0])-1] = int(self.dmx_queue[0][1])
                self.dmx_queue.pop(0)
            else:
                packet = packet_old

            self.a.set(packet)
            # print(self.dmx_queue)
            # print("EEEEEEEEEEEEEEEEEEEEEE")
            time.sleep(0.03)
            packet_old = packet
            if self.stop:
                break

    def change_value_for_channel(self, channel_raw:str, value, temp: bool):
        universe, channel = str(channel_raw).split(".")
        dmx_value = [channel, value]
        # print(dmx_value)
        self.dmx_queue.append(dmx_value)
        time.sleep(0.03)  # timing issues here / also so gehts iwie, aber gut ist anders
        ####### timing issues!!!!  die queue sendet nur mit 30fps und wenn hier dann mehr kommt, wird die voll bzw unendlich voll
        ##TODO: fix timing issues


        #t = time.time()
        if not temp:
            # change value in the dmx_output file
            # read file
            with open("internal_files/dmx_output.json") as f:
                data = json.load(f)

            # change value for desired channel
            data[universe][channel] = int(value)

            # safe to file again
            with open("internal_files/dmx_output.json", "w") as f:
                json.dump(data, f, indent=4, separators=(',', ': '))

        #ti = time.time()
        #print("Time wirte json" + str(ti-t))

    def generate_empty_dmx_output_file(self):
        data = {}
        empty_universe = {}
        for channel in range(1, 513, 1):
            empty_universe[str(channel)] = 0

        for universe in range(3):
            data[universe] = empty_universe

        with open("internal_files/dmx_output.json", "w") as f:
            json.dump(data, f, indent=4, separators=(',', ': '))




    #### the following fuctions are only for the hardware communication ####

    def start_input_hardware(self):
        universe = 14  # hardware positions are on sub 1 u 14
        self.listener = self.ai.register_listener(universe, sub=1, net=0, is_simplified=False)

    def read_input_hardware(self):
        buffer = self.ai.get_buffer(self.listener)
        return buffer

    def start_output_hardware(self) -> None:
        self.ah = StupidArtnet()
        self.ai = StupidArtnetServer()
        self.output_thread_h = threading.Thread()
        self.hardware_dmx_queue = [[1, 0]]
        self.stop_h = False

        target_ip = "255.255.255.255"
        universe = 15
        self.ah = StupidArtnet(target_ip, universe, 120, 40, True, True)
        self.ah.set_simplified(False)
        self.ah.set_net(0)
        self.ah.set_subnet(1)
        print(self.ah)  # print the init log of StupidArtnet
        self.ah.start()

        self.output_thread_h = threading.Thread(target=self.build_output_package_hardware, name="Outputter_Hardware")
        self.output_thread_h.start()

    def build_output_package_hardware(self):
        packet = bytearray(120)
        packet_old = bytearray(120)

        for x in range(120):
            packet[x] = 0
            packet_old[x] = 0

        while True:
            if len(self.hardware_dmx_queue) > 0:
                # print(self.dmx_queue)
                packet[int(self.hardware_dmx_queue[0][0]) - 1] = int(self.hardware_dmx_queue[0][1])
                self.hardware_dmx_queue.pop(0)
            else:
                packet = packet_old
            # print(packet)
            self.ah.set(packet)
            # print(self.dmx_queue)
            time.sleep(0.03)
            packet_old = packet
            if self.stop_h:
                break

    def change_value_for_channel_hardware(self, channel: int, value: int):
        dmx_value = [channel, value]
        print(" ## Hardware: " + str(dmx_value))
        self.hardware_dmx_queue.append(dmx_value)

    ### end ###


# A = ArtnetManager(512)
# A.start_output()
# input("Press Enter to start output")
# A.generate_empty_dmx_output_file()

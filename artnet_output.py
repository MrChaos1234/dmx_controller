from stupidArtnet import StupidArtnet
import random
import time
import threading
import json


class ArtnetOutputter:
    def __init__(self, packet_size):
        self.a = StupidArtnet()
        self.packet_size = packet_size
        self.output_thread = threading.Thread()
        self.dmx_queue = [[1, 0]]
        self.stop = False

    def start_output(self) -> None:
        target_ip = "255.255.255.255"
        packet_size = self.packet_size # only even numbers are working
        universe = 15
        self.a = StupidArtnet(target_ip, universe, packet_size, 40, True, True)
        self.a.set_simplified(False)
        self.a.set_net(0)
        self.a.set_subnet(1)
        print(self.a)  # print the init log of StupidArtnet
        self.a.start()

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
            time.sleep(0.03)
            packet_old = packet
            if self.stop:
                break

    def change_value_for_channel(self, channel_raw:str, value, temp: bool):
        universe, channel = str(channel_raw).split(".")
        dmx_value = [channel, value]
        print(dmx_value)
        self.dmx_queue.append(dmx_value)

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

    def generate_empty_dmx_output_file(self):
        data = {}
        empty_universe = {}
        for channel in range(1, 513, 1):
            empty_universe[str(channel)] = 0

        for universe in range(3):
            data[universe] = empty_universe

        with open("internal_files/dmx_output.json", "w") as f:
            json.dump(data, f, indent=4, separators=(',', ': '))


# A = ArtnetOutputter(512)
# A.generate_empty_dmx_output_file()

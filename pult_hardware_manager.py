import json
import os
import threading
import time

from artnet_manager import ArtnetManager


class PultHardwareManager:
    def __init__(self):
        self.max_faders = 10
        self.max_buttons = 10
        self.fader_states: list = [0] * self.max_faders  # for a max of 10 faders
        self.button_states: list = [0] * self.max_buttons  # for a max of 10 buttons
        self.backand_hardware_artnet_manager = ArtnetManager(512)

        self.backand_hardware_artnet_manager.start_output_hardware()

        self.backand_hardware_artnet_manager.start_input_hardware()
        input_thread = threading.Thread(target=self.read_hardware_values)
        input_thread.start()

    def read_hardware_values(self):
        while True:
            buffer = self.backand_hardware_artnet_manager.read_input_hardware()

            if buffer is not None:
                if len(buffer) > 0:
                    for x in range(self.max_faders):
                        self.fader_states[x] = buffer[x]
                    for x in range(self.max_buttons):
                        self.button_states[x] = (buffer[x + 100])

                    time.sleep(0.0000001)  # here is also some weird timing issue.. with the sleep it works, without not

    # following are the functions to call from frontEnd
    def get_fader_value(self, fader_number):
        fader_number = fader_number - 1
        return self.fader_states[fader_number]

    def set_fader_value(self, fader_number, value):
        self.backand_hardware_artnet_manager.change_value_for_channel_hardware(fader_number, value)

    def get_button_value(self, button_number):
        button_number = button_number - 1
        if self.button_states[button_number] == 255:
            return 1
        else:
            return 0



# P = PultHardwareManager()
# input("Press Enter to continue...")
# print(P.get_fader_value(1))
# P.set_fader_value(1, 100)


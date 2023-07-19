from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
from py_managers.artnet_manager import ArtnetManager
from py_managers.cue_manager import CueManager
from py_managers.dmx_data_generation_manager import DmxDataGenerationManager
from py_managers.fixture_manager import FixtureManager
from py_drivers.driver_set_fader_to_position_thread import DriverSetFaderToPositionThread

import threading

import time


class FaderPage(QObject):

    active_page_id_changed: pyqtSignal = pyqtSignal(int)

    change_effect_speed: pyqtSignal = pyqtSignal(int, int)
    change_effect_fade: pyqtSignal = pyqtSignal(int, int)

    change_dimmer_channel: pyqtSignal = pyqtSignal(int, int)
    change_color_red_channel: pyqtSignal = pyqtSignal(int, int)
    change_color_green_channel: pyqtSignal = pyqtSignal(int, int)
    change_color_blue_channel: pyqtSignal = pyqtSignal(int, int)

    set_fader_0_to_position: pyqtSignal = pyqtSignal(int)
    set_fader_1_to_position: pyqtSignal = pyqtSignal(int)
    set_fader_2_to_position: pyqtSignal = pyqtSignal(int)
    set_fader_3_to_position: pyqtSignal = pyqtSignal(int)
    
    
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self._cue_manager = CueManager()
        self._dmx_data_generation_manager = DmxDataGenerationManager()
        self.fader_cue_relation = self._cue_manager.get_fader_cue_relation()
        
        self.faders_moving: bool = False
        self.faders_blocked: bool = False
        
        self.active_page_id: int = 0

        self.current_fader_positions: list = [10, 10, 10, 10]

        self.fader_positions: list = [[10, 10, 10, 10], [10, 10, 10, 10], [10, 10, 10, 10], [10, 10, 10, 10]]
        

    def setup(self) -> None:
        # set faders to zero!
        desired_positions: list = [6, 6, 6, 6]
        self.move_faders_to_desired_position(desired_positions)

    @pyqtSlot(object, int)
    def faderPosition0_updated_handler(self, object, fader_position):
        self.current_fader_positions[0] = fader_position

    @pyqtSlot(object, int)
    def faderPosition1_updated_handler(self, object, fader_position):
        self.current_fader_positions[1] = fader_position

    @pyqtSlot(object, int)
    def faderPosition2_updated_handler(self, object, fader_position):
        self.current_fader_positions[2] = fader_position

    @pyqtSlot(object, int)
    def faderPosition3_updated_handler(self, object, fader_position):
        self.current_fader_positions[3] = fader_position

    @pyqtSlot()
    def block_unblock_faders_handler(self) -> None:
        if self.faders_blocked:
            self.faders_blocked = False
        else:
            self.faders_blocked = True
    
    @pyqtSlot()
    def page_up_handler(self) -> None:
        # dont do anything if faders are still moving
        if self.faders_moving:
            print("Faders are still moving, wait a second")
            return
        
        # set the new active page id
        self.faders_moving = True
        new_active_page_id: int = self.active_page_id + 1
        if new_active_page_id > 3:
            new_active_page_id = 3
            
        # save current fader positions
        #print("self.current_fader_positions: " + str(self.current_fader_positions))
        #print("Saving: " + str(self.current_fader_positions) + " to page: " + str(self.active_page_id))
        #print("self.active_page_id: " + str(self.active_page_id))
        #print("Fader positions before change: " + str(self.fader_positions))
        self.fader_positions[self.active_page_id] = self.current_fader_positions.copy()
        #print("Fader positions after change: " + str(self.fader_positions))

        # update fader positions
        desired_positions: list = self.fader_positions[new_active_page_id]
        # print("Desired positions: " + str(desired_positions))
        self.move_faders_to_desired_position(desired_positions)
        
        # update active page id
        self.active_page_id += 1
        if self.active_page_id > 3:
            self.active_page_id = 3
        self.active_page_id_changed.emit(self.active_page_id)

    @pyqtSlot()
    def page_down_handler(self) -> None:
        # dont do anything if faders are still moving
        if self.faders_moving:
            print("Faders are still moving, wait a second")
            return
        # set the new active page id
        new_active_page_id: int = self.active_page_id - 1
        if new_active_page_id < 0:
            new_active_page_id = 0
        # save current fader positions
        self.fader_positions[self.active_page_id] = self.current_fader_positions.copy()

        # update fader positions
        self.faders_moving = True
        desired_positions: list = self.fader_positions[new_active_page_id]
        self.move_faders_to_desired_position(desired_positions)
        
        # update active page id
        self.active_page_id -= 1
        if self.active_page_id < 0:
            self.active_page_id = 0
        self.active_page_id_changed.emit(self.active_page_id)

    @pyqtSlot()
    def faders_moving_done_handler(self):
        self.faders_moving = False
            
    @pyqtSlot(int, int, int)
    def fader_page_position_changed_handler(self, channel_id: int, position: int, active_page_id: int):
        # print("Fader page position changed handler called for channel: " + str(channel_id) + " with position: " + str(position) + " on page: " + str(active_page_id))
        if self.faders_moving:
            return
        else:
            for page in self.fader_cue_relation:
                if page["page_id"] == active_page_id:
                    for fader in page["fader_data"]:
                        if fader["fader_id"] == channel_id:
                            if fader["cue_id"] != "None":
                                if fader["fader_purpose"] == "dimmer":
                                    if self.faders_blocked:
                                        print("Faders are blocked")
                                        return
                                    self.change_dimmer_channel.emit(fader["cue_id"], position)
                                elif fader["fader_purpose"] == "red":
                                    if self.faders_blocked:
                                        print("Faders are blocked")
                                        return
                                    self.change_color_red_channel.emit(fader["cue_id"], position)
                                elif fader["fader_purpose"] == "green":
                                    if self.faders_blocked:
                                        print("Faders are blocked")
                                        return
                                    self.change_color_green_channel.emit(fader["cue_id"], position)
                                elif fader["fader_purpose"] == "blue":
                                    self.change_color_blue_channel.emit(fader["cue_id"], position)
                                    if self.faders_blocked:
                                        print("Faders are blocked")
                                        return

                            elif fader["effect"] != "None":
                                if "speed" in fader["effect"]:
                                    self.change_effect_speed.emit(int(fader["effect"][0]), position)
                                elif "fade" in fader["effect"]:
                                    self.change_effect_fade.emit(int(fader["effect"][0]), position)
                            else:
                                return

    def get_channel_info(self, channel_id: int, active_page_id) -> list:
        for page in self.fader_cue_relation:
            if page["page_id"] == active_page_id:
                for fader in page["fader_data"]:
                    if fader["fader_id"] == channel_id:
                        channel_info: str = ""
                        channel_icon_path: str = ""

                        if fader["cue_id"] != "None":
                            channel_info: str = f"Dimmer for cue: {fader['cue_id']}"
                            channel_icon_path: str = "../res/dimmer.png"
                        elif fader["effect"] != "None":
                            if "speed" in fader["effect"]:
                                channel_info: str = f"Speed for effect: {fader['effect'][0]}"
                                channel_icon_path: str = "../res/speed.png"
                            elif "fade" in fader["effect"]:
                                channel_info: str = f"Fade for effect: {fader['effect'][0]}"
                                channel_icon_path: str = "../res/speed.png"
                        else:
                            channel_info: str = ""
                            channel_icon_path: str = "../res/empty.png"

                        return [channel_info, channel_icon_path]

        return ["", "../res/empty.png"]

    def move_faders_to_desired_position(self, desired_positions: list):
        self._move_faders_thread = QThread()
        self._driver_set_fader_to_position_thread = DriverSetFaderToPositionThread(desired_positions)
        self._driver_set_fader_to_position_thread.moveToThread(self._move_faders_thread)
        self._move_faders_thread.started.connect(self._driver_set_fader_to_position_thread.run)
        self._driver_set_fader_to_position_thread.finished.connect(self._move_faders_thread.quit)
        self._driver_set_fader_to_position_thread.finished.connect(self.faders_moving_done_handler)
        
        self._driver_set_fader_to_position_thread.set_fader_0_to_position.connect(self.set_fader_0_to_position)
        self._driver_set_fader_to_position_thread.set_fader_1_to_position.connect(self.set_fader_1_to_position)
        self._driver_set_fader_to_position_thread.set_fader_2_to_position.connect(self.set_fader_2_to_position)
        self._driver_set_fader_to_position_thread.set_fader_3_to_position.connect(self.set_fader_3_to_position)
        
        self._move_faders_thread.start()
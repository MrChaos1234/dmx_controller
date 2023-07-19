from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot

from py_managers.artnet_manager import ArtnetManager
from py_components.artnet_output import ArtnetOutput

from py_components.fader_page import FaderPage


class FaderQmlPresentationModel(QObject):
    HYSTERESIS: int = 2
    
    faderPosition0_updated: pyqtSignal = pyqtSignal()
    faderPosition1_updated: pyqtSignal = pyqtSignal()
    faderPosition2_updated: pyqtSignal = pyqtSignal()
    faderPosition3_updated: pyqtSignal = pyqtSignal()

    set_position_set_value_0_triggered: pyqtSignal = pyqtSignal(int)
    set_position_set_value_1_triggered: pyqtSignal = pyqtSignal(int)
    set_position_set_value_2_triggered: pyqtSignal = pyqtSignal(int)
    set_position_set_value_3_triggered: pyqtSignal = pyqtSignal(int)

    setup_connection_0_triggered: pyqtSignal = pyqtSignal(str)
    cleanup_connection_0_triggered: pyqtSignal = pyqtSignal()
    set_faders_count_0_triggered: pyqtSignal = pyqtSignal(int)
    set_max_motor_stop_timeout_counter_0_triggered: pyqtSignal = pyqtSignal(
        int)
    
    fader_page_position_changed: pyqtSignal = pyqtSignal(int, int, int)
    
    update_fader_info: pyqtSignal = pyqtSignal()
        
    _last_fader_position_0: int
    _last_fader_position_1: int
    _last_fader_position_2: int
    _last_fader_position_3: int
    
    _faderPosition0: int
    _faderPosition1: int
    _faderPosition2: int
    _faderPosition3: int
    
    _last_fader_dmx_position_0: int
    _last_fader_dmx_position_1: int
    _last_fader_dmx_position_2: int
    _last_fader_dmx_position_3: int

    active_page_id: int
    
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._faderPosition0 = 0
        self._faderPosition1 = 0
        self._faderPosition2 = 0
        self._faderPosition3 = 0
        self._last_fader_position_0 = 0
        self._last_fader_position_1 = 0
        self._last_fader_position_2 = 0
        self._last_fader_position_3 = 0
        
        self._last_fader_dmx_position_0 = 0
        self._last_fader_dmx_position_1 = 0
        self._last_fader_dmx_position_2 = 0
        self._last_fader_dmx_position_3 = 0
        
        self.active_page_id = 0
        
        self._fader_page = FaderPage()
    
        
    @pyqtProperty(int, notify=faderPosition0_updated)
    def faderPosition0(self):
        return self._faderPosition0

    @faderPosition0.setter
    def faderPosition0(self, value: int):
        if self._faderPosition0 == value:
            return
        self._faderPosition0 = value
        self.faderPosition0_updated.emit()

    @pyqtProperty(int, notify=faderPosition1_updated)
    def faderPosition1(self):
        return self._faderPosition1

    @faderPosition1.setter
    def faderPosition1(self, value: int):
        if self._faderPosition1 == value:
            return
        self._faderPosition1 = value
        self.faderPosition1_updated.emit()

    @pyqtProperty(int, notify=faderPosition2_updated)
    def faderPosition2(self):
        return self._faderPosition2

    @faderPosition2.setter
    def faderPosition2(self, value: int):
        if self._faderPosition2 == value:
            return
        self._faderPosition2 = value
        self.faderPosition2_updated.emit()

    @pyqtProperty(int, notify=faderPosition3_updated)
    def faderPosition3(self):
        return self._faderPosition3

    @faderPosition3.setter
    def faderPosition3(self, value: int):
        if self._faderPosition3 == value:
            return
        self._faderPosition3 = value
        self.faderPosition3_updated.emit()

    @pyqtSlot(object, int)
    def position_fader0_changed(self, instance_data: object, position: int) -> None:
        if self._last_fader_position_0 == 0:
            self._last_fader_position_0 = position
            self.faderPosition0 = self.convertRawValueToDmx(position)
            self.fader_page_position_changed.emit(0, int(self.faderPosition0), self.active_page_id)
            self._last_fader_dmx_position_0 = self.faderPosition0
        else:
            if abs(self._last_fader_position_0 - position) >= self.HYSTERESIS:
                self._last_fader_position_0 = position
                self.faderPosition0 = self.convertRawValueToDmx(position)
                if self._last_fader_dmx_position_0 != self.faderPosition0:
                    self.fader_page_position_changed.emit(0, int(self.faderPosition0), self.active_page_id)
                    self._last_fader_dmx_position_0 = self.faderPosition0
                    
    @pyqtSlot(object, int)
    def position_fader1_changed(self, instance_data: object, position: int) -> None:
        if self._last_fader_position_1 == 0:
            self._last_fader_position_1 = position
            self.faderPosition1 = self.convertRawValueToDmx(position)
            self.fader_page_position_changed.emit(1, int(self.faderPosition1), self.active_page_id)
            self._last_fader_dmx_position_1 = self.faderPosition1
        else:
            if abs(self._last_fader_position_1 - position) >= self.HYSTERESIS:
                self._last_fader_position_1 = position
                self.faderPosition1 = self.convertRawValueToDmx(position)
                if self._last_fader_dmx_position_1 != self.faderPosition1:
                    self.fader_page_position_changed.emit(1, int(self.faderPosition1), self.active_page_id)
                    self._last_fader_dmx_position_1 = self.faderPosition1
                                    

    @pyqtSlot(object, int)
    def position_fader2_changed(self, instance_data: object, position: int) -> None:
        if self._last_fader_position_2 == 0:
            self._last_fader_position_2 = position
            self.faderPosition2 = self.convertRawValueToDmx(position)
            self.fader_page_position_changed.emit(2, int(self.faderPosition2), self.active_page_id)
            self._last_fader_dmx_position_2 = self.faderPosition2
        else:
            if abs(self._last_fader_position_2 - position) >= self.HYSTERESIS:
                self._last_fader_position_2 = position
                self.faderPosition2 = self.convertRawValueToDmx(position)
                if self._last_fader_dmx_position_2 != self.faderPosition2:
                    self.fader_page_position_changed.emit(2, int(self.faderPosition2), self.active_page_id)
                    self._last_fader_dmx_position_2 = self.faderPosition2

    @pyqtSlot(object, int)
    def position_fader3_changed(self, instance_data: object, position: int) -> None:
        if self._last_fader_position_3 == 0:
            self._last_fader_position_3 = position
            self.faderPosition3 = self.convertRawValueToDmx(position)
            self.fader_page_position_changed.emit(3, int(self.faderPosition3), self.active_page_id)
            self._last_fader_dmx_position_3 = self.faderPosition3
        else:
            if abs(self._last_fader_position_3 - position) >= self.HYSTERESIS:
                self._last_fader_position_3 = position
                self.faderPosition3 = self.convertRawValueToDmx(position)
                if self._last_fader_dmx_position_3 != self.faderPosition3:
                   self.fader_page_position_changed.emit(3, int(self.faderPosition3), self.active_page_id)
                   self._last_fader_dmx_position_3 = self.faderPosition3
                

    @pyqtSlot(int, int)
    def setPositionSetValue(self, faderIndex: int, positionSetValue: int) -> None:
        if faderIndex == 0:
            self.set_position_set_value_0_triggered.emit(positionSetValue)
        if faderIndex == 1:
            self.set_position_set_value_1_triggered.emit(positionSetValue)
        if faderIndex == 2:
            self.set_position_set_value_2_triggered.emit(positionSetValue)
        if faderIndex == 3:
            self.set_position_set_value_3_triggered.emit(positionSetValue)

    @pyqtSlot(int, str)
    def setupConnection(self, connectionIndex: int, serialPortDeviceName: str) -> None:
        if connectionIndex == 0:
            self.setup_connection_0_triggered.emit(serialPortDeviceName)

    @pyqtSlot(int)
    def cleanupConnection(self, connectionIndex: int) -> None:
        if connectionIndex == 0:
            self.cleanup_connection_0_triggered.emit()

    @pyqtSlot(int, int)
    def setFadersCount(self, connectionIndex: int, fadersCount: int) -> None:
        if connectionIndex == 0:
            self.set_faders_count_0_triggered.emit(fadersCount)

    @pyqtSlot(int, int)
    def setMaxMotorStopTimeoutCounter(self, connectionIndex: int, maxMotorStopTimeoutCounter: int) -> None:
        if connectionIndex == 0:
            self.set_max_motor_stop_timeout_counter_0_triggered.emit(
                maxMotorStopTimeoutCounter)

    def convertRawValueToDmx(self, raw_value: int) -> int:
        result: float = (raw_value - 12) * (255/(995-12))
        if result < 0.0:
            result = 0.0
        elif result > 255.0:
            result = 255.0
        return int(result)

    def active_page_id_changed_handler(self, active_page_id: int) -> None:
        self.active_page_id = active_page_id
        print("active page id changed to: " + str(active_page_id))
        self.update_fader_info.emit()
    
    @pyqtSlot(int, result=str)
    def get_channel_name(self, channel: int) -> str:
        channel_info = self._fader_page.get_channel_info(channel, self.active_page_id)
        return channel_info[0]

    @pyqtSlot(int, result=str)
    def get_channel_symbol(self, channel: int) -> str:
        channel_info = self._fader_page.get_channel_info(channel, self.active_page_id)
        return channel_info[1]
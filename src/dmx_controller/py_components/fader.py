from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from py_components.fader_controller_connection import FaderControllerConnection


class Fader(QObject):
    position_changed: pyqtSignal = pyqtSignal(object, int)  # Qt Signal emitted, if the position changes its value in between min and max
    
    _fader_controller_connection: FaderControllerConnection
    _fader_index: int
    _min: int  # minimal boundary for position
    _max: int  # maximal boundary for position
    _raw_min: int
    _raw_max: int
    _instance_data: object  # user defined data belonging to this instance of the Fader class

    def __init__(
        self,
        fader_controller_connection: FaderControllerConnection,
        fader_index: int,
        min: int = 0,
        max: int = 255,
        raw_min: int = 12,
        raw_max: int = 1007,
        instance_data: object = None,
        parent: QObject = None,
    ):
        super().__init__(parent)
        self._fader_controller_connection = fader_controller_connection
        self._fader_index = fader_index
        self._min = min
        self._max = max
        self._raw_min = raw_min
        self._raw_max = raw_max
        self._instance_data = instance_data
        # connect signals of fader controller hardware instance with slots
        self._fader_controller_connection.position_changed.connect(self._position_changed)

    @pyqtSlot(int, int)
    def _position_changed(self, fader_index: int, position: int) -> None:
        if fader_index == self._fader_index:
            self._notify_position_changed(position)

    def _notify_position_changed(self, raw_position: int) -> None:
        position: int = self._convert_raw_position(raw_position)
        self.position_changed.emit(self._instance_data, position)

    def _convert_raw_position(self, raw_position: int) -> int:
        position: int = int((raw_position - self._raw_min) / (self._raw_max - self._raw_min) * (self._max - self._min))
        if position < self._min:
            position = self._min
        elif position > self._max:
            position = self._max
        return position

    @pyqtSlot(int)
    def position_fader(self, new_position: int) -> None:
        print("position_fader() called with new_position = " + str(new_position))
        new_raw_position: int = self._convert_fader_stick_position(new_position)
        self._fader_controller_connection.position_fader(self._fader_index, new_raw_position)

    def _convert_fader_stick_position(self, fader_stick_position: int) -> int:
        raw_position: int = int(self._raw_min + fader_stick_position * (self._raw_max - self._raw_min) / (self._max - self._min))
        if raw_position < self._raw_min:
            raw_position = self._raw_min
        elif raw_position > self._raw_max:
            raw_position = self._raw_max
        return raw_position

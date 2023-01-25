from PyQt5.QtCore import QObject, pyqtSignal

from py_drivers.driver_rotary_encoder import GpioBasedRotaryEncoderDriver


class RotaryEncoder(QObject):

    position_changed: pyqtSignal = pyqtSignal(object, int)
    min_changed: pyqtSignal = pyqtSignal(object, int)
    max_changed: pyqtSignal = pyqtSignal(object, int)
    pushbutton_pressed: pyqtSignal = pyqtSignal(object)
    pushbutton_released: pyqtSignal = pyqtSignal(object)
    state_changed: pyqtSignal = pyqtSignal(object, int)

    _rotary_encoder_driver: GpioBasedRotaryEncoderDriver # the rotary encoder hardware instance, that is used to realize this rotary encoder instance
    _position: int
    _min: int
    _max: int
    _state: int
    _instance_data: object # user defined data belonging to this instance of the RotaryEncoder class

    def __init__(self,
                 rotary_encoder_driver: GpioBasedRotaryEncoderDriver,
                 position: int = 0,
                 min: int = 0,
                 max: int = 255,
                 instance_data: object = None,
                 parent: QObject = None):
        super().__init__(parent)
        self._rotary_encoder_driver = rotary_encoder_driver
        self._position = position
        self._min = min
        self._max = max
        self._state = 0
        self._instance_data = instance_data
        self._rotary_encoder_driver.rotated_clockwise.connect(self._rotated_clockwise)
        self._rotary_encoder_driver.rotated_counterclockwise.connect(self._rotated_counterclockwise)
        self._rotary_encoder_driver.pushbutton_pressed.connect(self._pushbutton_pressed)
        self._rotary_encoder_driver.pushbutton_released.connect(self._pushbutton_released)

    def setup(self) -> None:
        self._rotary_encoder_driver.setup()

    def _rotated_clockwise(self, instance_data: object) -> None:
        if self._instance_data == instance_data:
            old_position: int = self._position
            self._position += 1
            if self._position > self._max:
                self._position = self._max
            if old_position != self._position:
                self._notify_position_changed()

    def _notify_position_changed(self):
        self.position_changed.emit(self._instance_data, self._position)

    def _rotated_counterclockwise(self, instance_data: object) -> None:
        if self._instance_data == instance_data:
            old_position: int = self._position
            self._position -= 1
            if self._position < self._min:
                self._position = self._min
            if old_position != self._position:
                self._notify_position_changed()

    def _pushbutton_pressed(self, instance_data: object) -> None:
        if self._instance_data == instance_data:
            self.pushbutton_pressed.emit(self._instance_data)

    def _pushbutton_released(self, instance_data: object) -> None:
        if self._instance_data == instance_data:
            if self._state == 1:
                self._state = 0
            else:
                self._state = 1
            self.pushbutton_released.emit(self._instance_data)
            self.state_changed.emit(self._instance_data, self._state)

    def setMin(self, newValue: int) -> None:
        if self._min != newValue:
            self._min = newValue
            self.min_changed.emit(self._instance_data, self._min)

    def setMax(self, newValue: int) -> None:
        if self._max != newValue:
            self._max = newValue
            self.max_changed.emit(self._instance_data, self._max)

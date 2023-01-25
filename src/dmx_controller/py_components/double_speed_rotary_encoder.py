from PyQt5.QtCore import QObject, pyqtSignal

from py_drivers.driver_rotary_encoder import GpioBasedRotaryEncoderDriver


class DoubleSpeedRotaryEncoder(QObject):

    is_in_double_speed_mode_changed: pyqtSignal = pyqtSignal(object, bool)
    position_changed: pyqtSignal = pyqtSignal(object, int)

    _rotary_encoder_driver: GpioBasedRotaryEncoderDriver # the rotary encoder hardware instance, that is used to realize this double speed rotary encoder instance
    _is_in_double_speed_mode: bool # if True, encoder increments/decrements are calculated in step width 10, else in step width 1
    _position: int # calculated encoder position, ranges from 0..255
    _instance_data: object # user defined data belonging to this instance of the DoubleSpeedRotaryEncoder class

    def __init__(self,
                 rotary_encoder_driver: GpioBasedRotaryEncoderDriver,
                 instance_data: object = None,
                 parent: QObject = None):
        super().__init__(parent)
        self._rotary_encoder_driver = rotary_encoder_driver
        self._is_in_double_speed_mode = False
        self._position = 0
        self._instance_data = instance_data
        self._rotary_encoder_driver.rotated_clockwise.connect(self.rotated_clockwise)
        self._rotary_encoder_driver.rotated_counterclockwise.connect(self.rotated_counterclockwise)
        self._rotary_encoder_driver.pushbutton_pressed.connect(self.pushbutton_pressed)
        self._rotary_encoder_driver.pushbutton_released.connect(self.pushbutton_released)

    def setup(self) -> None:
        self._rotary_encoder_driver.setup()

    def rotated_clockwise(self, instance_data: object) -> None:
        if self._instance_data == instance_data:
            old_position: int = self._position
            if self._is_in_double_speed_mode:
                self._position += 10
            else:
                self._position += 1
            if self._position > 255:
                self._position = 255
            if old_position != self._position:
                self._notify_position_changed()

    def _notify_position_changed(self):
        self.position_changed.emit(self._instance_data, self._position)

    def rotated_counterclockwise(self, instance_data: object) -> None:
        if self._instance_data == instance_data:
            old_position: int = self._position
            if self._is_in_double_speed_mode:
                self._position -= 10
            else:
                self._position -= 1
            if self._position < 0:
                self._position = 0
            if old_position != self._position:
                self._notify_position_changed()

    def pushbutton_pressed(self, instance_data: object) -> None:
        pass

    def pushbutton_released(self, instance_data: object) -> None:
        self.toggle_is_in_double_speed_mode(instance_data)

    def toggle_is_in_double_speed_mode(self, instance_data: object) -> None:
        if self._instance_data == instance_data:
            self._is_in_double_speed_mode = not self._is_in_double_speed_mode
            self.is_in_double_speed_mode_changed.emit(self._instance_data, self._is_in_double_speed_mode)

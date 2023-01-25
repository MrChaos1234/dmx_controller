from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot


class DoubleSpeedRotaryEncoderQmlPresentationModel(QObject):

    position_updated: pyqtSignal = pyqtSignal()
    is_in_double_speed_mode_updated: pyqtSignal = pyqtSignal()

    is_in_double_speed_mode_toggled: pyqtSignal = pyqtSignal(object)

    _position: int
    _is_in_double_speed_mode: bool
    _instance_data: object

    def __init__(self, instance_data: object = None,
                       parent: QObject = None):
        super().__init__(parent)
        self._instance_data = instance_data
        self._position = 0
        self._is_in_double_speed_mode = False

    @pyqtProperty(int, notify=position_updated)
    def position(self) -> int:
        return self._position

    @position.setter
    def position(self, value: int) -> None:
        if self._position == value:
            return
        self._position = value
        self.position_updated.emit()

    @pyqtProperty(int, notify=is_in_double_speed_mode_updated)
    def is_in_double_speed_mode(self) -> bool:
        return self._is_in_double_speed_mode

    @is_in_double_speed_mode.setter
    def is_in_double_speed_mode(self, value: bool) -> None:
        if self._is_in_double_speed_mode == value:
            return
        self._is_in_double_speed_mode = value
        self.is_in_double_speed_mode_updated.emit()

    def is_in_double_speed_mode_changed(self, instance_data: object, is_in_double_speed_mode: bool) -> None:
        if instance_data == self._instance_data:
            self.is_in_double_speed_mode = is_in_double_speed_mode

    def position_changed(self, instance_data: object, position: int) -> None:
        if instance_data == self._instance_data:
            self.position = position

    @pyqtSlot()
    def toggle_is_in_double_speed_mode(self) -> None:
        self.is_in_double_speed_mode_toggled.emit(self._instance_data)

from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class RotaryEncoderPresentationModel(QObject):

    position_updated: pyqtSignal = pyqtSignal()
    min_updated: pyqtSignal = pyqtSignal()
    max_updated: pyqtSignal = pyqtSignal()
    pushbutton_pressed: pyqtSignal = pyqtSignal()
    pushbutton_released: pyqtSignal = pyqtSignal()
    state_updated: pyqtSignal = pyqtSignal()
    # purpose_updated: pyqtSignal = pyqtSignal()

    _position: int
    _min: int
    _max: int
    _state: int
    # _purpose: str

    def __init__(self, parent=None):
        super().__init__(parent)
        self._position = 0
        self._min = -10
        self._max = 10
        self._state = 0
        self._purpose = 'None'

    @pyqtProperty(int, notify=position_updated)
    def position(self):
        return self._position

    @position.setter
    def position(self, value: int):
        if self._position == value:
            return
        self._position = value
        self.position_updated.emit()

    @pyqtProperty(int, notify=min_updated)
    def min(self):
        return self._min

    @min.setter
    def min(self, value: int):
        if self._min == value:
            return
        self._min = value
        self.min_updated.emit()

    @pyqtProperty(int, notify=max_updated)
    def max(self):
        return self._max

    @max.setter
    def max(self, value: int):
        if self._max == value:
            return
        self._max = value
        self.max_updated.emit()

    def press_pushbutton(self):
        self.pushbutton_pressed.emit()

    def release_pushbutton(self):
        self.pushbutton_released.emit()

    @pyqtProperty(int, notify=state_updated)
    def state(self):
        return self._state

    @state.setter
    def state(self, value: int):
        if self._state == value:
            return
        self._state = value
        self.state_updated.emit()

    # @pyqtProperty(str, notify=purpose_updated)
    # def purpose(self):
    #     return self._purpose

    # @state.setter
    # def purpose(self, value: str):
    #     if self._purpose == value:
    #         return
    #     self._purpose = value
    #     self.purpose_updated.emit()

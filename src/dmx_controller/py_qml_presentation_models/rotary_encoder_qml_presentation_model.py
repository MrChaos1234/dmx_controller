from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


##### not used




class RotaryEncoderQmlPresentationModel(QObject):

    position_updated: pyqtSignal = pyqtSignal()
    min_updated: pyqtSignal = pyqtSignal()
    max_updated: pyqtSignal = pyqtSignal()
    pushbutton_pressed: pyqtSignal = pyqtSignal()
    pushbutton_released: pyqtSignal = pyqtSignal()
    state_updated: pyqtSignal = pyqtSignal()

    _position: int
    _min: int
    _max: int
    _state: int
    _instance_data: object

    def __init__(self, instance_data: object = None,
                       parent=None):
        super().__init__(parent)
        self._instance_data = instance_data
        self._position = 0
        self._min = 0
        self._max = 255
        self._state = 0

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
    
    def press_pushbutton(self, instance_data: object):
        if instance_data == self._instance_data:
            self.pushbutton_pressed.emit()

    def release_pushbutton(self, instance_data: object):
        if instance_data == self._instance_data:
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

    def position_changed(self, instance_data: object, position: int) -> None:
        if instance_data == self._instance_data:
            self.position = position

    def min_changed(self, instance_data: object, min: int) -> None:
        if instance_data == self._instance_data:
            self.min = min

    def max_changed(self, instance_data: object, max: int) -> None:
        if instance_data == self._instance_data:
            self.max = max

    def state_changed(self, instance_data: object, state: int) -> None:
        if instance_data == self._instance_data:
            self.state = state

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from i2c_thread import I2cThread


class KKeypad(QObject):

    key_pressed: pyqtSignal = pyqtSignal(int)  # signal to emit when a key is pressed
    key_released: pyqtSignal = pyqtSignal(int)  # signal to emit when a key is released

    _i2c_thread: I2cThread

    def __init__(self,
                 i2c_thread: I2cThread,
                 parent: QObject = None):
        super().__init__(parent)
        self._i2c_thread = i2c_thread
        self._i2c_thread.key_pressed.connect(self.key_pressed_handler)
        self._i2c_thread.key_released.connect(self.key_released_handler)

    @pyqtSlot(int)
    def key_pressed_handler(self, key_number: int) -> None:
        print("keypad")
        self.key_pressed.emit(key_number)

    @pyqtSlot(int)
    def key_released_handler(self, key_number: int) -> None:
        self.key_released.emit(key_number)

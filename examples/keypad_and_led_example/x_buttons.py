from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from i2c_thread import I2cThread


class XButtons(QObject):

    # signal to emit when a key is pressed
    x_key_pressed: pyqtSignal = pyqtSignal(int)
    # signal to emit when a key is released
    x_key_released: pyqtSignal = pyqtSignal(int)

    _i2c_thread: I2cThread

    def __init__(self,
                 i2c_thread: I2cThread,
                 parent: QObject = None):
        super().__init__(parent)
        self._i2c_thread = i2c_thread
        self._i2c_thread.x_key_pressed.connect(self.x_key_pressed_handler)
        self._i2c_thread.x_key_released.connect(self.x_key_released_handler)

    @pyqtSlot(int)
    def x_key_pressed_handler(self, key_number: int) -> None:
        self.x_key_pressed.emit(key_number)

    @pyqtSlot(int)
    def x_key_released_handler(self, key_number: int) -> None:
        self.x_key_released.emit(key_number)

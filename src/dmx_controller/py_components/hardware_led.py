from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from threads.i2c_thread import I2cThread


class HardwareLed(QObject):

    hardware_led_color_change: pyqtSignal = pyqtSignal(int, int, int, int)  # signal to emit when the color of a led should be changed
    
    def __init__(self,
                 i2c_thread: I2cThread,
                 parent: QObject = None):
        super().__init__(parent)
        
    @pyqtSlot(int, int, int, int)
    def change_led_color(self, led_number: int, r: int, g: int, b: int):
        self.hardware_led_color_change.emit(led_number, r, g, b)
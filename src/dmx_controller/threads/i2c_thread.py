from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot, QThread
from time import sleep

from smbus import SMBus

from py_drivers.driver_k_keypad import I2cKeypadDriver
from py_drivers.driver_led import I2cLedDriver

from py_drivers.driver_x_buttons import XButtonsDriver


class I2cThread(QThread):
    WAIT_TIME: float = 0.04
    # signal to emit when a key is pressed
    key_pressed: pyqtSignal = pyqtSignal(int)
    # signal to emit when a key is released
    key_released: pyqtSignal = pyqtSignal(int)

    # signal to emit when a key is pressed
    x_key_pressed: pyqtSignal = pyqtSignal(int)
    # signal to emit when a key is released
    x_key_released: pyqtSignal = pyqtSignal(int)

    i2c_bus: SMBus
    i2c_keypad: I2cKeypadDriver
    i2c_led: I2cLedDriver
    x_buttons: XButtonsDriver

    # user defined data belonging to this instance of the DoubleSpeedRotaryEncoder class
    _instance_data: object

    def __init__(self,
                 parent: QObject = None,
                 led_value_to_change: list = None):
        super().__init__(parent)
        # threading.Thread.__init__(self)

    def run(self):
        print("I2C Thread LEVEL: I2cThread.run() called")

        self.i2c_bus = SMBus(1)

        # create an instance of the I2cKeypad class
        self.i2c_keypad = I2cKeypadDriver(self.i2c_bus, self._key_pressed_callback, self._key_released_callback)
        # create an instance of the I2cLed class
        # self.i2c_led = I2cLedDriver(self.i2c_bus)
        # create an instance of the XButtons class
        self.x_buttons = XButtonsDriver(self.i2c_bus, self._x_key_pressed_callback, self._x_key_released_callback)

        # runs infinitely until the stop_event is set
        while True:
            self.i2c_keypad.check_for_change()
            self.x_buttons.check_for_change()
            sleep(self.WAIT_TIME)

    def stop_and_wait(self) -> None:
        # signal the thread to stop
        # wait until the thread stopped
        while self.is_alive():
            sleep(0.01)

    # callbacks that are called by the I2cKeypad class

    def _key_pressed_callback(self, key_number: int) -> None:
        # callback emits the key_pressed signal and passes the key number as an argument
        self.key_pressed.emit(key_number)

    def _key_released_callback(self, key_number: int) -> None:
        self.key_released.emit(key_number)

    # callbacks that are called by the XButtons class
    def _x_key_pressed_callback(self, key_number: int) -> None:
        # callback emits the key_pressed signal and passes the key number as an argument
        self.x_key_pressed.emit(key_number)

    def _x_key_released_callback(self, key_number: int) -> None:
        self.x_key_released.emit(key_number)

    @pyqtSlot(int, int, int, int)
    def led_color_change_handler(self, number: int, r: int, g: int, b: int) -> None:
        self.i2c_led.change_led_color(number, r, g, b)

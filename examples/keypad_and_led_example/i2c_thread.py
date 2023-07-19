from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import time
import threading

from smbus import SMBus

from driver_k_keypad import I2cKeypad
from driver_led import I2cLed

from driver_x_buttons import XButtons

class I2cThread(QObject, threading.Thread):

    key_pressed: pyqtSignal = pyqtSignal(int)  # signal to emit when a key is pressed
    key_released: pyqtSignal = pyqtSignal(int)  # signal to emit when a key is released

    x_key_pressed: pyqtSignal = pyqtSignal(int)  # signal to emit when a key is pressed
    x_key_released: pyqtSignal = pyqtSignal(int)  # signal to emit when a key is released
    
    stop_event: threading.Event  # event to signal the thread that it should stop
    i2c_bus: SMBus
    i2c_keypad: I2cKeypad
    i2c_led: I2cLed
    x_buttons: XButtons
    
    _instance_data: object # user defined data belonging to this instance of the DoubleSpeedRotaryEncoder class

    def __init__(self, 
                 parent: QObject = None, 
                 led_value_to_change: list = None):
        super().__init__(parent)
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
                

    def run(self):
        self.stop_event.clear()

        self.i2c_bus = SMBus(1)

        self.i2c_keypad = I2cKeypad(self.i2c_bus, self._key_pressed_callback, self._key_released_callback) # create an instance of the I2cKeypad class
        self.i2c_led = I2cLed(self.i2c_bus) # create an instance of the I2cLed class
        self.x_buttons = XButtons(self.i2c_bus, self._x_key_pressed_callback, self._x_key_released_callback) # create an instance of the XButtons class
        
        # runs infinitely until the stop_event is set
        while not self.stop_event.is_set():
            self.i2c_keypad.check_for_change()
            self.x_buttons.check_for_change()
            

    def stop_and_wait(self) -> None:
        # signal the thread to stop
        self.stop_event.set()
        # wait until the thread stopped
        while self.is_alive():
            time.sleep(0.01)
    
    
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
        print("I2C Thread LEVEL: I2cThread.led_color_change_handler() called with arguments: number = {}, r = {}, g = {}, b = {}".format(number, r, g, b))
        self.i2c_led.change_led_color(number, r, g, b)
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from threads.i2c_thread import I2cThread
from pynput.keyboard import Key, Controller
import time


class KKeypad(QObject):

    # signal to emit when a key is pressed
    key_pressed: pyqtSignal = pyqtSignal(int)
    # signal to emit when a key is released
    key_released: pyqtSignal = pyqtSignal(int)

    clear_output_key: pyqtSignal = pyqtSignal()
    
    start_effect: pyqtSignal = pyqtSignal(int)
    stop_effect: pyqtSignal = pyqtSignal(int)
    
    _i2c_thread: I2cThread

    def __init__(self,
                 i2c_thread: I2cThread,
                 parent: QObject = None):
        super().__init__(parent)
        self._i2c_thread = i2c_thread

        self._keyboard = Controller()

        self.effect_1_running = False
        self.effect_2_running = False
        self.effect_3_running = False
        self.effect_4_running = False
        
    @pyqtSlot()
    def setup(self) -> None:
        self._i2c_thread.key_pressed.connect(self.key_pressed_handler)
        self._i2c_thread.key_released.connect(self.key_released_handler)

    @pyqtSlot(int)
    def key_pressed_handler(self, key_number: int) -> None:
        print("key " + str(key_number) + " pressed")

        if key_number == 1:
            self._keyboard.press("0")
            # time.sleep(0.01)
            self._keyboard.release("0")
        if key_number == 5:
            self._keyboard.press("1")
            # time.sleep(0.01)
            self._keyboard.release("1")
        if key_number == 6:
            self._keyboard.press("2")
            # time.sleep(0.01)
            self._keyboard.release("2")
        if key_number == 7:
            self._keyboard.press("3")
            # time.sleep(0.01)
            self._keyboard.release("3")
        if key_number == 9:
            self._keyboard.press("4")
            # time.sleep(0.01)
            self._keyboard.release("4")
        if key_number == 10:
            self._keyboard.press("5")
            # time.sleep(0.01)
            self._keyboard.release("5")
        if key_number == 11:
            self._keyboard.press("6")
            # time.sleep(0.01)
            self._keyboard.release("6")
        if key_number == 13:
            self._keyboard.press("7")
            # time.sleep(0.01)
            self._keyboard.release("7")
        if key_number == 14:
            self._keyboard.press("8")
            # time.sleep(0.01)
            self._keyboard.release("8")
        if key_number == 15:
            self._keyboard.press("9")
            # time.sleep(0.01)
            self._keyboard.release("9")

        if key_number == 2:
            self._keyboard.press(".")
            # time.sleep(0.01)
            self._keyboard.release(".")

        if key_number == 4:
            #self.clear_output_key.emit()
            self._keyboard.type(Key.alt + Key.f4)
            # doing just some stuff to crash the program


        if key_number == 3:
            self._keyboard.press(Key.backspace)
            # time.sleep(0.1)
            self._keyboard.release(Key.backspace)

        if key_number == 17:
            if self.effect_1_running:
                self.stop_effect.emit(1)
                self.effect_1_running = False
            else:
                self.start_effect.emit(1)
                self.effect_1_running = True
                
        if key_number == 18:
            if self.effect_2_running:
                self.stop_effect.emit(2)
                self.effect_2_running = False
            else:
                self.start_effect.emit(2)
                self.effect_2_running = True
                
        if key_number == 19:
            if self.effect_3_running:
                self.stop_effect.emit(3)
                self.effect_3_running = False
            else:
                self.start_effect.emit(3)
                self.effect_3_running = True
                
        if key_number == 20:
            if self.effect_4_running:
                self.stop_effect.emit(4)
                self.effect_4_running = False
            else:
                self.start_effect.emit(4)
                self.effect_4_running = True


        self.key_pressed.emit(key_number)

    @pyqtSlot(int)
    def key_released_handler(self, key_number: int) -> None:
        self.key_released.emit(key_number)

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread
import time


class DriverSetFaderToPositionThread(QObject):
    set_fader_0_to_position: pyqtSignal = pyqtSignal(int)
    set_fader_1_to_position: pyqtSignal = pyqtSignal(int)
    set_fader_2_to_position: pyqtSignal = pyqtSignal(int)
    set_fader_3_to_position: pyqtSignal = pyqtSignal(int)
    
    finished: pyqtSignal = pyqtSignal()
    
    _desired_positions: list
    
    def __init__(self, desired_positions: list, parent: QObject = None):
        super().__init__(parent)
        self._desired_positions = desired_positions
        
    def run(self):        
        self.set_fader_0_to_position.emit(int(self._desired_positions[0]))
        self.set_fader_1_to_position.emit(int(self._desired_positions[1]))
        self.set_fader_2_to_position.emit(int(self._desired_positions[2]))
        self.set_fader_3_to_position.emit(int(self._desired_positions[3]))
        
        time.sleep(0.3) # approx the max time that a fader will take to move
        
        self.finished.emit()

        
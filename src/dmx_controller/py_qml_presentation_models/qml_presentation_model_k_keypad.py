from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class KKeypadQmlPresentationModel(QObject):

    key_pressed: pyqtSignal = pyqtSignal(int)  # signal to emit when a key is pressed
    key_released: pyqtSignal = pyqtSignal(int)  # signal to emit when a key is released

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

    @pyqtSlot(int)
    def key_pressed_handler(self, key_number: int) -> None:
        print("keypad muss hier durch")
        self.key_pressed.emit(key_number)

    @pyqtSlot(int)
    def key_released_handler(self, key_number: int) -> None:
        self.key_released.emit(key_number)

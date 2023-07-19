from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot


class ColorPickerQmlPresentationModel(QObject):

    r_updated: pyqtSignal = pyqtSignal()
    g_updated: pyqtSignal = pyqtSignal()
    b_updated: pyqtSignal = pyqtSignal()
    dimmer_updated: pyqtSignal = pyqtSignal()
    
    mixed_color_updated: pyqtSignal = pyqtSignal(int, int, int)

    _r: int
    _g: int
    _b: int 
    _dimmer: int

    def __init__(self, instance_data: object = None,
                       parent: QObject = None):
        super().__init__(parent)
        self._r = 0
        self._g = 0
        self._b = 0
        self._dimmer = 0

    @pyqtProperty(int, notify=r_updated)
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, value: int) -> None:
        if self._r == value:
            return
        self._r = value
        self.r_updated.emit()

    @pyqtProperty(int, notify=g_updated)
    def g(self) -> int:
        return self._g

    @g.setter
    def g(self, value: int) -> None:
        if self._g == value:
            return
        self._g = value
        self.g_updated.emit()

    @pyqtProperty(int, notify=b_updated)
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value: int) -> None:
        if self._b == value:
            return
        self._b = value
        self.b_updated.emit()

    @pyqtProperty(int, notify=dimmer_updated)
    def dimmer(self) -> int:
        return self._dimmer

    @dimmer.setter
    def dimmer(self, value: int) -> None:
        if self._dimmer == value:
            return
        self._dimmer = value
        self.dimmer_updated.emit()

    @pyqtSlot(int)
    def r_changed(self, r: int) -> None:
        self.r = r

    @pyqtSlot(int)
    def g_changed(self, g: int) -> None:
        self.g = g

    @pyqtSlot(int)
    def b_changed(self, b: int) -> None:
        self.b = b
        
    @pyqtSlot(int)
    def dimmer_changed(self, dimmer: int) -> None:
        self.dimmer = dimmer

    @pyqtSlot(int, int, int)
    def mixed_color_changed(self, r: int, g: int, b: int) -> None:
        self.mixed_color_updated.emit(r, g, b)

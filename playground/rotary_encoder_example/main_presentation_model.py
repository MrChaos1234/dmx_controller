from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class MainPresentationModel(QObject):

    foo_updated: pyqtSignal = pyqtSignal()

    _foo: int

    def __init__(self, parent=None):
        super().__init__(parent)
        self._foo = 0

    @pyqtProperty(int, notify=foo_updated)
    def foo(self):
        return self._foo

    @foo.setter
    def foo(self, value: int):
        if self._foo == value:
            return
        self._foo = value
        self.foo_updated.emit()

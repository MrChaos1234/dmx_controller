from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class StageViewQmlPresentationModel(QObject):

    made_change: pyqtSignal = pyqtSignal(list)
    
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

    @pyqtSlot(list)
    def save_view(self, data: list) -> None:
        self.made_change.emit(data)


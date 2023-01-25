from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class StageView(QObject):
    made_change: pyqtSignal = pyqtSignal(list)

    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        
   
    @pyqtSlot(list)
    def made_change_handler(self, data: list) -> None:
        print("StageView: updated")


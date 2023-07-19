from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class ArtnetOutputQmlPresentationModel(QObject):
    
    clear_output_requested: pyqtSignal = pyqtSignal()
    execute_cue_requested: pyqtSignal = pyqtSignal(int) 
    clear_cue_requested: pyqtSignal = pyqtSignal(int)
        
    def __init__(self, parent: QObject = None):
        super().__init__(parent)

    @pyqtSlot()
    def clear_output(self):
        print("clear output requested")
        self.clear_output_requested.emit()
    
    @pyqtSlot(int)
    def execute_cue(self, cue_index: int):
        # print("execute cue id " + str(cue_index) + " requested")
        self.execute_cue_requested.emit(cue_index)
        
    @pyqtSlot(int)
    def clear_cue(self, cue_index: int):
        # print("clear cue id " + str(cue_index) + " requested")
        self.clear_cue_requested.emit(cue_index)
    
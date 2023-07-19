from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class EffectsQmlPresentationModel(QObject):
    
    start_effect_requested = pyqtSignal(int)
    stop_effect_requested = pyqtSignal(int)
    
    set_effect_cues_requested: pyqtSignal = pyqtSignal(int, list)    
    update_effect_cues_requested: pyqtSignal = pyqtSignal()
    
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.effect_cues = []

    @pyqtSlot(int)
    def start_effect(self, effect_id: int):
        self.start_effect_requested.emit(effect_id)
    
    @pyqtSlot(int)
    def stop_effect(self, effect_id: int):
        self.stop_effect_requested.emit(effect_id)
    
    @pyqtSlot(int, str, result=bool)
    def set_effect_cues(self, effect_id: int, cues: str):
        try:
            cues = [int(cue) for cue in cues.split('.')]
        except ValueError:
            cues = []
            
        self.set_effect_cues_requested.emit(effect_id, cues)
        
        return True
    
    @pyqtSlot()
    def update_effect_cues(self):
        self.update_effect_cues_requested.emit()
        
    @pyqtSlot(list)
    def effect_cues_updated_handler(self, cues: list):
        self.effect_cues = cues
    
    @pyqtSlot(int, result=str)
    def get_effect_cues(self, effect_id:int):
        return ".".join([str(cue) for cue in self.effect_cues[effect_id - 1]])
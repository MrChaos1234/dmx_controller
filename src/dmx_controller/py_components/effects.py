from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from py_managers.effects_manager import EffectsManager


class Effects(QObject):

    set_effect_speed_fader: pyqtSignal = pyqtSignal(int)
    set_effect_fade_fader: pyqtSignal = pyqtSignal(int)

    effect_cues_updated: pyqtSignal = pyqtSignal(list)
    
    block_unblock_faders: pyqtSignal = pyqtSignal()
    
    def __init__(self, effects_manager: EffectsManager, parent: QObject = None):
        super().__init__(parent)
        self._effects_manager = effects_manager
        self.speed = 5
        self.fade = 0
        
        self.speed_blocker = False
        self.fade_blocker = False

    @pyqtSlot(int)
    def start_effect_handler(self, effect_id: int) -> None:
        self.block_unblock_faders.emit()
        self._effects_manager.run_effect(effect_id)
        
    @pyqtSlot(int)
    def stop_effect_handler(self, effect_id: int) -> None:
        self.block_unblock_faders.emit()
        self._effects_manager.stop_effect(effect_id)

    @pyqtSlot(int, int)
    def set_effect_speed_handler(self, effect: int, raw_speed: int) -> None:
        if self.speed_blocker:
            print("speed blocked")
            return
        
        self.speed = abs(raw_speed - 255) / 50
        if self.speed < 0.2:
            self.speed = 0.2

        self._effects_manager.set_effect_speed(effect, self.speed)

    @pyqtSlot(int, int)
    def set_effect_fade_handler(self, effect: int, raw_fade: int) -> None:
        if self.fade_blocker:
            print("fade blocked")
            return
        
        self.fade = raw_fade / 50
        if self.fade <= 0.2:
            self.fade = 0

        if self.fade > self.speed - 0.3:
            # print("fade too high")
            self.fade = 0

        self._effects_manager.set_effect_fade(effect, self.fade)

    @pyqtSlot(int, list)
    def set_effect_cues_handler(self, effect_id: int, cues: list) -> None:
        self._effects_manager.set_effect_cues(effect_id, cues)
        
    @pyqtSlot()
    def get_effect_cues(self):
        self.effect_cues_updated.emit(self._effects_manager.get_effect_cues())
        
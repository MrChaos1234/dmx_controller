from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from py_managers.cue_manager import CueManager, Cue


class CueList(QObject):
    cues_changed: pyqtSignal = pyqtSignal(object)
    _cue_manager: CueManager

    button_grid_view_changed: pyqtSignal = pyqtSignal(list)
    
    cue_list_updated: pyqtSignal = pyqtSignal(list)
    
    def __init__(self, cue_manager: CueManager, parent: QObject = None,):
        super().__init__(parent)
        self._cue_manager = cue_manager
        self._cues = []
        self._selected_cues = {}

    def setup(self) -> None:
        self._get_cues()
        self._notify_cues_changed()
        self.update_button_grid_view_handler()

    def _get_cues(self) -> None:
        cues_data: list[dict] = self._cue_manager.get_cues()
        self._cues.clear()
        cue_data: dict
        for cue_data in cues_data:
            cue: Cue = Cue(cue_data)
            self._cues.append(cue)

    def _notify_cues_changed(self) -> None:
        self.cues_changed.emit(self._cues)

    @pyqtSlot()
    def start_setup_handler(self) -> None:
        self.setup()
        
    @pyqtSlot(int)
    def change_cue_selected_status_handler(self, index) -> None:
        # set the status value
        try:
            if self._selected_cues[index]:
                # if the cue is already selected, we have to set the status to false
                self._selected_cues[index] = False
            elif not self._selected_cues[index]:
                # if the cue is not selected, we have to set the status to true
                self._selected_cues[index] = True
        except KeyError:
            # if this is the case, its the first time the cue is selected, so we have to set the status to true
            self._selected_cues[index] = True

        # genereate the new cue list
        cues_data: list[dict] = self._cue_manager.get_cues()
        self._cues.clear()
        cue_data: dict
        i = 0
        selected = False
        for cue_data in cues_data:
            try:
                selected = self._selected_cues[i]
            except KeyError:
                pass
            fixture: Cue = Cue(cue_data, selected)
            self._cues.append(fixture)
            i += 1
            selected = False

        # notify the view
        self._notify_cues_changed()

    @pyqtSlot(object)
    def add_cue_handler(self, cue: Cue) -> None:
        self._cue_manager.add_cue(cue.id, cue.cue_name, cue.cue_group, cue.data)
        self._get_cues()
        self._notify_cues_changed()

    @pyqtSlot(int)
    def remove_cue_handler(self, index) -> None:
        # remove the fixture from the json file with fixture manager
        self._cue_manager.remove_cue(index)
        self._selected_cues = {}  # reset the selected fixtures
        self._get_cues()  # reload fixtures
        self._notify_cues_changed()  # notify the view

    @pyqtSlot()
    def update_cue_list_handler(self) -> None:
        self._get_cues()  # reload fixtures
        self._notify_cues_changed()  # notify the view

    pyqtSlot()
    def update_button_grid_view_handler(self) -> None:
        button_grid_view = self._cue_manager.update_button_grid_view()
        self.button_grid_view_changed.emit(button_grid_view)
        
    @pyqtSlot(int, int)
    def add_tile_cue_relation_handler(self, tile_index, cue_index) -> None:
        self._cue_manager.add_tile_cue_relation(tile_index, cue_index)
        self.update_button_grid_view_handler()
    
    @pyqtSlot(int)
    def remove_tile_cue_relation_handler(self, tile_index) -> None:
        self._cue_manager.remove_tile_cue_relation(tile_index)
        self.update_button_grid_view_handler()
                
    @pyqtSlot()
    def get_cue_list_handler(self) -> None:
        data = self._cue_manager.get_cues()
        self.cue_list_updated.emit(data)
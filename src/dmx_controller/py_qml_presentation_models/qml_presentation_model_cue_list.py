import json
from PyQt5.QtCore import Qt, QObject, QAbstractListModel, QModelIndex, pyqtSignal, pyqtSlot

from py_qml_presentation_models.qml_presentation_model_cue import CueQmlPresentationModel
from py_managers.cue_manager import Cue, CueManager
from py_managers.dmx_data_generation_manager import DmxDataGenerationManager

class CueListQmlPresentationModel(QAbstractListModel):
    updated: pyqtSignal = pyqtSignal()
    add_cue_requested: pyqtSignal = pyqtSignal(object)
    remove_cue_requested: pyqtSignal = pyqtSignal(int)

    update_cue_list_requested: pyqtSignal = pyqtSignal()
    change_cue_selected_status: pyqtSignal = pyqtSignal(int)

    _cues_qml_presentation_models: list[CueQmlPresentationModel]

    update_currentCueId: pyqtSignal = pyqtSignal(str)
    update_currentCueName: pyqtSignal = pyqtSignal(str)

    update_button_grid_view_requested: pyqtSignal = pyqtSignal()
    check_cue_tile_relation_requested: pyqtSignal = pyqtSignal(int)

    add_tile_cue_relation_requested: pyqtSignal = pyqtSignal(int, int)
    remove_tile_cue_relation_requested: pyqtSignal = pyqtSignal(int)

    get_cue_list_requested: pyqtSignal = pyqtSignal()

    block_unblock_faders: pyqtSignal = pyqtSignal()
    
    def __init__(self, cues_qml_presentation_models: list[CueQmlPresentationModel], parent: QObject = None):
        super().__init__(parent)
        self._cues_qml_presentation_models = cues_qml_presentation_models
        self._button_grid_view = []
        self._cue_list = []
        self._button_grid_edit_mode = False
        self._button_grid_reaction_mode1 = False
        self._button_grid_reaction_mode2 = False
        self._cue_manager = CueManager()
        self._dmx_data_generation_manager = DmxDataGenerationManager()
        
        self.pressed_buttons = []

    def rowCount(self, parent: QObject = None, *args, **kwargs):
        return len(self._cues_qml_presentation_models)

    def data(self, index: QModelIndex, role=None):
        if role == Qt.DisplayRole:
            return self._cues_qml_presentation_models[index.row()]

    @pyqtSlot(int)
    def update_current_index(self, index: int) -> None:
        cues = self._cue_manager.get_cues()

        i = 0
        for cue in cues:
            if i == index:
                self.update_currentCueId.emit(str(cue["id"]))
                self.update_currentCueName.emit(str(cue["cue_name"]))
                break
            i += 1

    @pyqtSlot(object)
    def cues_changed(self, cues: list[Cue]) -> None:
        self.beginResetModel()
        self._cues_qml_presentation_models.clear()

        cue: Cue
        for cue in cues:
            self._cues_qml_presentation_models.append(CueQmlPresentationModel(str(cue.id), str(
                cue.cue_name), str(cue.cue_group), cue.data, cue.selected, self))

        self.endResetModel()
        self.updated.emit()

    @pyqtSlot(int)
    def select(self, index: int) -> None:
        # the function can select and deselect a fixture -> if selected, just call again to deselect
        self.change_cue_selected_status.emit(index)

    @pyqtSlot(str, str, str)
    def add_cue(self, cueId: str, cueName: str, cueGroup: str) -> None:
        print("Add cue called")
        
        data: list = self._dmx_data_generation_manager.get_temp_cue_data()
        _cue_data = {"id": cueId,
                     "cue_name": cueName,
                     "cue_group": cueGroup,
                     "data": data}
        _cue: Cue = Cue(_cue_data)
        self.add_cue_requested.emit(_cue)
    

    @pyqtSlot()
    def remove_selected_cues(self) -> None:
        print("Remove selected cues")
        cues_indexes_to_remove: list[int] = []
        # fill the list with the indexes of the selected fixtures
        for index in range(len(self._cues_qml_presentation_models)):
            if self._cues_qml_presentation_models[index].selected:
                cues_indexes_to_remove.append(
                    int(self._cues_qml_presentation_models[index].identifier))

        for cue_index in cues_indexes_to_remove:
            self.remove_cue_requested.emit(cue_index)

    @pyqtSlot()
    def update_fixture_patch(self):
        print("Update fixture patch")
        self.update_cue_list_requested.emit()

    @pyqtSlot()
    def update_button_grid_view(self):
        print("Update button grid view")
        self.update_button_grid_view_requested.emit()

    @pyqtSlot(list)
    def button_grid_view_changed_handler(self, button_grid_view: list):
        self._button_grid_view = button_grid_view

    @pyqtSlot(int, result=str)
    def find_tile_cue_relation(self, tile_id: int) -> bool:
        self.update_button_grid_view_requested.emit()

        for dict in self._button_grid_view:
            if dict["tile_id"] == tile_id:
                return str(dict["cue_id"])

    @pyqtSlot(int, int)
    def add_tile_cue_relation(self, tile_id: int, cue_id: int):
        self.add_tile_cue_relation_requested.emit(tile_id, cue_id)

    @pyqtSlot(int)
    def remove_tile_cue_relation(self, tile_id: int):
        self.remove_tile_cue_relation_requested.emit(tile_id)

    @pyqtSlot(list)
    def cue_list_updated_handler(self, cue_list: list):
        self._cue_list = cue_list

    @pyqtSlot(result=list)
    def get_cue_list(self) -> str:
        self.get_cue_list_requested.emit()
        return self._cue_list

    @pyqtSlot(bool)
    def set_button_grid_edit_mode(self, edit_mode: bool):
        self._button_grid_edit_mode = edit_mode

    @pyqtSlot(result=bool)
    def get_button_grid_edit_mode(self) -> bool:
        return self._button_grid_edit_mode
    
    @pyqtSlot(bool)
    def set_button_grid_reaction_mode_1(self, reaction_mode: bool):
       self._button_grid_reaction_mode1 = reaction_mode

    @pyqtSlot(result=bool)
    def get_button_grid_reaction_mode_1(self) -> bool:
        return self._button_grid_reaction_mode1
    
    @pyqtSlot(bool)
    def set_button_grid_reaction_mode_2(self, reaction_mode: bool):
       self._button_grid_reaction_mode2 = reaction_mode

    @pyqtSlot(result=bool)
    def get_button_grid_reaction_mode_2(self) -> bool:
        return self._button_grid_reaction_mode2
    
    @pyqtSlot(int, bool)
    def set_button_state(self, id, state):
        print("set button state called " + str(id) + " " + str(state))
        if state:
            self.pressed_buttons.append(id)
            self.block_unblock_faders.emit()
        else:
            self.pressed_buttons.remove(id)
            self.block_unblock_faders.emit()
            
    @pyqtSlot(int, result=bool)
    def get_button_state(self, id):
        print("pressed buttons: " + str(self.pressed_buttons))
        if id in self.pressed_buttons:
            return True
        else:
            return False

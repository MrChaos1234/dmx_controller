from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class CueQmlPresentationModel(QObject):

    identifier_updated: pyqtSignal = pyqtSignal()
    cue_name_updated: pyqtSignal = pyqtSignal()
    cue_group_updated: pyqtSignal = pyqtSignal()
    data_updated: pyqtSignal = pyqtSignal()
    selected_updated: pyqtSignal = pyqtSignal()
    
    _id: str
    _cue_name: str
    _cue_group: str
    _data: dict
   
    def __init__(self, cue_id: str, cue_name: str, cue_group: str, data: dict, selected: bool, parent: QObject = None):
        super().__init__(parent)
        self._id = cue_id
        self._cue_name = cue_name
        self._cue_group = cue_group
        self._data = data
        self._selected = selected
            
    # ID
    @pyqtProperty(str, notify=identifier_updated)
    def identifier(self) -> str:
        return self._id

    @identifier.setter
    def identifier(self, value: str) -> None:
        if self._id == value:
            return
        self._id = value
        self.identifier_updated.emit()

    # Name
    @pyqtProperty(str, notify=cue_name_updated)
    def cue_name(self) -> str:
        return self._cue_name

    @cue_name.setter
    def cue_name(self, value: str) -> None:
        if self._cue_name == value:
            return
        self._cue_name = value
        self.cue_name_updated.emit()

    # Group
    @pyqtProperty(str, notify=cue_group_updated)
    def cue_group(self) -> str:
        return self._cue_group

    @cue_group.setter
    def cue_group(self, value: str) -> None:
        if self._cue_group == value:
            return
        self._cue_group = value
        self.cue_group_updated.emit()

    # Data
    @pyqtProperty(dict, notify=data_updated)
    def data(self) -> dict:
        return self._data

    @data.setter
    def data(self, value: dict) -> None:
        if self._data == value:
            return
        self._data = value
        self.data_updated.emit()

    # Selected
    @pyqtProperty(bool, notify=selected_updated)
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        if self.selected == value:
            return
        self._selected = value
        self.selected_updated.emit()

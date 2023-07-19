from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class FixtureQmlPresentationModel(QObject):

    identifier_updated: pyqtSignal = pyqtSignal()
    fixture_name_updated: pyqtSignal = pyqtSignal()
    fixture_library_id_updated: pyqtSignal = pyqtSignal()
    fixture_display_name_updated: pyqtSignal = pyqtSignal()
    channel_mode_updated: pyqtSignal = pyqtSignal()
    dmx_start_address_updated: pyqtSignal = pyqtSignal()
    selected_updated: pyqtSignal = pyqtSignal()
    in_stage_view_updated: pyqtSignal = pyqtSignal()

    _id: str
    _fixture_name: str
    _fixture_library_id: str
    _fixture_display_name: str
    _channel_mode: str
    _dmx_start_address: str
    _in_stage_view: str

    def __init__(self, fixture_id: str, fixture_name: str, fixture_library_id: str, fixture_display_name: str, channel_mode: str, dmx_start_address: str, in_stage_view: str, selected: bool, parent: QObject = None):
        super().__init__(parent)
        self._id = fixture_id
        self._fixture_name = fixture_name
        self._fixture_library_id = fixture_library_id
        self._fixture_display_name = fixture_display_name
        self._channel_mode = channel_mode
        self._dmx_start_address = dmx_start_address
        self._selected = selected
        if in_stage_view == "True":
            self._in_stage_view = True
        else:
            self._in_stage_view = False

    
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
    @pyqtProperty(str, notify=fixture_name_updated)
    def fixture_name(self) -> str:
        return self._fixture_name

    @fixture_name.setter
    def fixture_name(self, value: str) -> None:
        if self._fixture_name == value:
            return
        self._fixture_name = value
        self.fixture_name_updated.emit()

    # Fixture Library ID
    @pyqtProperty(str, notify=fixture_library_id_updated)
    def fixture_library_id(self) -> str:
        return self._fixture_library_id

    @fixture_library_id.setter
    def fixture_library_id(self, value: str) -> None:
        if self._fixture_library_id == value:
            return
        self._fixture_library_id = value
        self.fixture_library_id_updated.emit()

    # Fixture Display Name
    @pyqtProperty(str, notify=fixture_display_name_updated)
    def fixture_display_name(self) -> str:
        return self._fixture_display_name

    @fixture_display_name.setter
    def fixture_display_name(self, value: str) -> None:
        if self._fixture_display_name == value:
            return
        self._fixture_display_name = value
        self.fixture_display_name_updated.emit()

    # Channel Mode
    @pyqtProperty(str, notify=channel_mode_updated)
    def channel_mode(self) -> str:
        return self._channel_mode

    @channel_mode.setter
    def channel_mode(self, value: str) -> None:
        if self._channel_mode == value:
            return
        self._channel_mode = value
        self.channel_mode_updated.emit()

    # DMX Start Address

    @pyqtProperty(str, notify=dmx_start_address_updated)
    def dmx_start_address(self) -> str:
        return self._dmx_start_address

    @dmx_start_address.setter
    def dmx_start_address(self, value: str) -> None:
        if self.dmx_start_address == value:
            return
        self._dmx_start_address = value
        self.dmx_start_address_updated.emit()

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

    # In Stage View
    @pyqtProperty(bool, notify=in_stage_view_updated)
    def in_stage_view(self) -> bool:
        return self._in_stage_view

    @in_stage_view.setter
    def in_stage_view(self, value: bool) -> None:
        if self.selected == value:
            return
        self._in_stage_view = value
        self.in_stage_view_updated.emit()


class LibraryFixtureQmlPresentationModel(QObject):

    id_updated: pyqtSignal = pyqtSignal()
    name_updated: pyqtSignal = pyqtSignal()

    _id: str
    _name: str

    def __init__(self, id: str, name: str, parent: QObject = None):
        super().__init__(parent)
        self._id = id
        self._name = name

    # id

    @pyqtProperty(str, notify=id_updated)
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        if self._id == value:
            return
        self._id = value
        self.id_updated.emit()

    # Name
    @pyqtProperty(str, notify=name_updated)
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if self._name == value:
            return
        self._name = value
        self.name_updated.emit()

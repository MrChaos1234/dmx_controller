from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty


class DmxChannelQmlPresentationModel(QObject):
    channel_id_updated: pyqtSignal = pyqtSignal()
    fixture_id_updated: pyqtSignal = pyqtSignal()
    fixture_display_name_updated: pyqtSignal = pyqtSignal()
    fixture_channel_mode_updated: pyqtSignal = pyqtSignal()
    
    _channel_id: str
    _fixture_id: str
    _fixture_display_name: str
    _fixture_channel_mode: str
    

    def __init__(self, channel_id: str, fixture_id: str, fixture_display_name: str, fixture_channel_mode: str, parent: QObject = None):
        super().__init__(parent)
        self._channel_id = channel_id
        self._fixture_id = fixture_id
        self._fixture_display_name = fixture_display_name
        self._fixture_channel_mode = fixture_channel_mode

    # Channel ID
    @pyqtProperty(str, notify=channel_id_updated)
    def channel_id(self) -> str:
        return self._channel_id

    @channel_id.setter
    def channel_id(self, value: str) -> None:
        if self._channel_id == value:
            return
        self._channel_id = value
        self.channel_id_updated.emit()
        
    # Fixture ID
    @pyqtProperty(str, notify=fixture_id_updated)
    def fixture_id(self) -> str:
        return self._fixture_id

    @fixture_id.setter
    def fixture_id(self, value: str) -> None:
        if self._fixture_id == value:
            return
        self._fixture_id = value
        self.fixture_id_updated.emit()

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
        
    # Fixture Channel Mode
    @pyqtProperty(str, notify=fixture_channel_mode_updated)
    def fixture_channel_mode(self) -> str:
        return self._fixture_channel_mode

    @fixture_channel_mode.setter
    def fixture_channel_mode(self, value: str) -> None:
        if self._fixture_channel_mode == value:
            return
        self._fixture_channel_mode = value
        self.fixture_channel_mode_updated.emit()
     
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from py_managers.fixture_manager import FixtureManager, Fixture, Channel


class DmxList(QObject):
    dmx_data_changed: pyqtSignal = pyqtSignal(object)
    _fixture_manager: FixtureManager

    def __init__(self, fixture_manager: FixtureManager, parent: QObject = None,):
        super().__init__(parent)
        self._fixture_manager = fixture_manager
        self._channel_values = []

    def setup(self) -> None:
        self._get_channel_values()
        self._notify_channel_values_changed()

    def _get_channel_values(self) -> None:
        data_of_all_channels: dict = self._fixture_manager.calculate_dmx_patch()
        self._channel_values.clear()
        for channel in data_of_all_channels:
            channel: Channel = Channel(channel, data_of_all_channels[channel][0], data_of_all_channels[channel][1], data_of_all_channels[channel][2])
            self._channel_values.append(channel)

    def _notify_channel_values_changed(self) -> None:
        self.dmx_data_changed.emit(self._channel_values)
       
        
    

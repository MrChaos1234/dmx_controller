from PyQt5.QtCore import Qt, QObject, QAbstractListModel, QModelIndex, pyqtSignal, pyqtSlot

from py_qml_presentation_models.qml_presentation_model_dmx_channel import DmxChannelQmlPresentationModel
from py_managers.fixture_manager import Fixture, Channel


class DmxListQmlPresentationModel(QAbstractListModel):

    updated: pyqtSignal = pyqtSignal()
   
    _dmx_universe_presentation_models: list[DmxChannelQmlPresentationModel]

    def __init__(self, dmx_universe_presentation_models: list[DmxChannelQmlPresentationModel], parent: QObject = None):
        super().__init__(parent)
        self._dmx_universe_presentation_models = dmx_universe_presentation_models

    def rowCount(self, parent: QObject = None, *args, **kwargs):
        return len(self._dmx_universe_presentation_models)

    def data(self, index: QModelIndex, role=None):
        if role == Qt.DisplayRole:
            return self._dmx_universe_presentation_models[index.row()]

    @pyqtSlot(object)
    def list_updated(self, channel_values: list) -> None:
        self.beginResetModel()
        self._dmx_universe_presentation_models.clear()
        channel: Channel
        
        for channel in channel_values:
            self._dmx_universe_presentation_models.append(DmxChannelQmlPresentationModel(channel.id, str(channel.fixture_id), channel.fixture_display_name, channel.fixture_channel_name))
        
        self.endResetModel()
        self.updated.emit()


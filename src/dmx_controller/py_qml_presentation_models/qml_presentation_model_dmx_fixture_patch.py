from PyQt5.QtCore import Qt, QObject, QAbstractListModel, QModelIndex, pyqtSignal, pyqtSlot

from py_qml_presentation_models.qml_presentation_model_fixture import FixtureQmlPresentationModel
from py_managers.fixture_manager import Fixture


class DmxFixturePatchQmlPresentationModel(QAbstractListModel):

    updated: pyqtSignal = pyqtSignal()
    add_fixture_requested: pyqtSignal = pyqtSignal(object)
    remove_fixture_requested: pyqtSignal = pyqtSignal(int)
    
    change_fixture_selected_status: pyqtSignal = pyqtSignal(int)

    update_fixture_patch_requested: pyqtSignal = pyqtSignal()
    
    _fixture_qml_presentation_models: list[FixtureQmlPresentationModel]
    
    def __init__(self, fixture_qml_presentation_models: list[FixtureQmlPresentationModel], parent: QObject = None):
        super().__init__(parent)
        self._fixture_qml_presentation_models = fixture_qml_presentation_models
        self.coordinates = [0, 0]

    def rowCount(self, parent: QObject = None, *args, **kwargs):
        return len(self._fixture_qml_presentation_models)

    def data(self, index: QModelIndex, role=None):
        if role == Qt.DisplayRole:
            return self._fixture_qml_presentation_models[index.row()]

    @pyqtSlot(object)
    def fixtures_changed(self, fixtures: list[Fixture]) -> None:
        self.beginResetModel()
        self._fixture_qml_presentation_models.clear()
        fixture: Fixture
        for fixture in fixtures:
            # print(str(fixture.id) + " " + str(fixture.fixture_name) + " " + str(fixture.fixture_library_id) + " " + str(fixture.display_name) + " " + str(fixture.channel_mode) + " " + str(fixture.dmx_start_address) + " " + str(fixture.in_stage_view) + "\n")
            self._fixture_qml_presentation_models.append(FixtureQmlPresentationModel(str(fixture.id),
                                                                                     str(
                                                                                         fixture.fixture_name),
                                                                                     str(
                                                                                         fixture.fixture_library_id),
                                                                                     str(
                                                                                         fixture.display_name),
                                                                                     str(
                                                                                         fixture.channel_mode),
                                                                                     str(
                                                                                         fixture.dmx_start_address),
                                                                                     str(
                                                                                         fixture.in_stage_view),
                                                                                     fixture.selected,
                                                                                     self))

            # print("Fixture: " + str(fixture.id) + " " + str(fixture.fixture_name) + " " + str(fixture.fixture_library_id) + " " +
            #       str(fixture.display_name) + " " + str(fixture.channel_mode) + " " + str(fixture.dmx_start_address) + " " + str(fixture.selected) + " " + str(fixture.in_stage_view) + "\n")

        self.endResetModel()
        self.updated.emit()

    @pyqtSlot(int)
    def select(self, index: int) -> None:
        # the function can select and deselect a fixture -> if selected, just call again to deselect
        self.change_fixture_selected_status.emit(index)

    @pyqtSlot(str, str, str, str, str, str)
    def add_fixture(self, fixtureType: str,
                    fixtureLibraryId: str,
                    fixtureId: str,
                    fixtureName: str,
                    fixtureMode: str,
                    fixtureDmxAddress: str) -> None:

        _fixture_data = {"id": fixtureId,
                         "fixture_name": fixtureType,
                         "fixture_library_id": fixtureLibraryId,
                         "display_name": fixtureName,
                         "channel_mode": fixtureMode,
                         "dmx_start_address": fixtureDmxAddress}

        _fixture: Fixture
        _fixture = Fixture(_fixture_data)

        self.add_fixture_requested.emit(_fixture)

    @pyqtSlot()
    def remove_selected_fixtures(self) -> None:
        print("Remove selected fixtures")
        fixture_indexes_to_remove: list[int] = []
        # fill the list with the indexes of the selected fixtures
        for index in range(len(self._fixture_qml_presentation_models)):
            if self._fixture_qml_presentation_models[index].selected:
                fixture_indexes_to_remove.append(
                    int(self._fixture_qml_presentation_models[index].identifier))

        print(fixture_indexes_to_remove)
        for fixture_index in fixture_indexes_to_remove:
            self.remove_fixture_requested.emit(fixture_index)

    @pyqtSlot()
    def update_fixture_patch(self):
        print("Update fixture patch")
        self.update_fixture_patch_requested.emit()
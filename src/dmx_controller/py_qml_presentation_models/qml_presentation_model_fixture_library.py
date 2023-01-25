from PyQt5.QtCore import Qt, QObject, QAbstractListModel, QModelIndex, pyqtSignal, pyqtSlot

from py_qml_presentation_models.qml_presentation_model_fixture import FixtureQmlPresentationModel, LibraryFixtureQmlPresentationModel
from py_managers.fixture_manager import Fixture, LibraryFixture, FixtureManager
from py_components.fixture_library import FixtureLibrary

class FixtureLibraryQmlPresentationModel(QAbstractListModel):

    updated: pyqtSignal = pyqtSignal()
    
    update_currentFixtureTypeName: pyqtSignal = pyqtSignal(str)
    update_currentFixtureTypeId: pyqtSignal = pyqtSignal(str)
    
    _library_fixture_qml_presentation_models: list[LibraryFixtureQmlPresentationModel]

    def __init__(self, library_fixture_qml_presentation_models: list[LibraryFixtureQmlPresentationModel], parent: QObject = None):
        super().__init__(parent)
        self._library_fixture_qml_presentation_models = library_fixture_qml_presentation_models

    def rowCount(self, parent: QObject = None, *args, **kwargs):
        return len(self._library_fixture_qml_presentation_models)

    def data(self, index: QModelIndex, role=None):
        if role == Qt.DisplayRole:
            return self._library_fixture_qml_presentation_models[index.row()]
    
    @pyqtSlot(object)
    def library_fixtures_changed(self, fixtures: list[LibraryFixture]) -> None:
        self.beginResetModel()
        self._library_fixture_qml_presentation_models.clear()
        library_fixture: LibraryFixture
        for library_fixture in fixtures:
            # print("Fixture: " + str(library_fixture.id) + " " + str(library_fixture.name))
            self._library_fixture_qml_presentation_models.append(LibraryFixtureQmlPresentationModel(str(library_fixture.id), str(library_fixture.name),  self))
        self.endResetModel()
        self.updated.emit()

    @pyqtSlot(int)
    def update_current_index(self, index: int) -> None:
        _fixture_manager: FixtureManager = FixtureManager()
        _fixture_library: FixtureLibrary = FixtureLibrary(_fixture_manager, self)
        fixtures = _fixture_library.get_fixtures_for_naming()
        library_fixture: LibraryFixture
        i = 0
        for library_fixture in fixtures:
            if index == i:
                self.update_currentFixtureTypeName.emit(library_fixture.name)
                self.update_currentFixtureTypeId.emit(str(library_fixture.id))
                break
            else:
                self.update_currentFixtureTypeName.emit("Index not found")
                self.update_currentFixtureTypeId.emit(str(library_fixture.id))
            i += 1
            


        
    
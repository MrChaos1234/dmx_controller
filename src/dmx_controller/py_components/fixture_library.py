from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from py_managers.fixture_manager import FixtureManager, Fixture, LibraryFixture


class FixtureLibrary(QObject):
    library_fixtures_changed: pyqtSignal = pyqtSignal(object)
    _fixture_manager: FixtureManager

    def __init__(self, fixture_manager: FixtureManager, parent: QObject = None,):
        super().__init__(parent)
        self._fixture_manager = fixture_manager
        self._library_fixtures = []

    def setup(self) -> None:
        self._get_fixtures()
        self._notify_library_fixtures_changed()

    def _get_fixtures(self) -> None:
        fixtures_data: dict = self._fixture_manager.list_available_fixtures()
        self._library_fixtures.clear()
        for id in fixtures_data:
            name = str(fixtures_data[id][0])
            fixture: LibraryFixture = LibraryFixture(str(id), name)
            self._library_fixtures.append(fixture)

    def _notify_library_fixtures_changed(self) -> None:
        self.library_fixtures_changed.emit(self._library_fixtures)

    def get_fixtures_for_naming(self) -> None:
        fixtures_data: dict = self._fixture_manager.list_available_fixtures()
        _library_fixtures = []
        for id in fixtures_data:
            name = str(fixtures_data[id][0])
            fixture: LibraryFixture = LibraryFixture(str(id), name)
            _library_fixtures.append(fixture)
        return _library_fixtures

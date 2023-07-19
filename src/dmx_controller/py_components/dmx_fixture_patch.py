from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from py_managers.fixture_manager import FixtureManager, Fixture


class DmxFixturePatch(QObject):
    fixtures_changed: pyqtSignal = pyqtSignal(object)
    _fixture_manager: FixtureManager

    def __init__(self, fixture_manager: FixtureManager, parent: QObject = None,):
        super().__init__(parent)
        self._fixture_manager = fixture_manager
        self._fixtures = []
        self._selected_fixtures = {}
        self.foo = 1

    def setup(self) -> None:
        self._get_fixtures()
        self._notify_fixtures_changed()

    def _get_fixtures(self) -> None:
        fixtures_data: list[dict] = self._fixture_manager.calculate_fixture_patch()
        self._fixtures.clear()
        fixture_data: dict
        for fixture_data in fixtures_data:
            # print("DATA: " + str(fixture_data) + "\n")
            fixture: Fixture = Fixture(fixture_data)
            self._fixtures.append(fixture)

    def _notify_fixtures_changed(self) -> None:
        self.fixtures_changed.emit(self._fixtures)
       
        
    @pyqtSlot(int)
    def change_fixture_selected_status_handler(self, index) -> None:
        # set the status value
        try:
            if self._selected_fixtures[index]:
                # if the fixture is already selected, we have to set the status to false
                self._selected_fixtures[index] = False
            elif not self._selected_fixtures[index]:
                # if the fixture is not selected, we have to set the status to true
                self._selected_fixtures[index] = True
        except KeyError:
            # if this is the case, its the first time the fixture is selected, so we have to set the status to true
            self._selected_fixtures[index] = True
        
        # genereate the new fixture list
        fixtures_data: list[dict] = self._fixture_manager.calculate_fixture_patch()
        self._fixtures.clear()
        fixture_data: dict
        i = 0
        selected = False
        for fixture_data in fixtures_data:
            try:
                selected = self._selected_fixtures[i]
            except KeyError:
                pass
            # print("DATA: " + str(fixture_data) + "\n")
            fixture: Fixture = Fixture(fixture_data, selected)
            self._fixtures.append(fixture)
            i += 1
            selected = False
        
        # notify the view
        self._notify_fixtures_changed()
    
    @pyqtSlot(object)
    def add_fixture_handler(self, fixture: Fixture) -> None:
        self._fixture_manager.add_fixture(fixture.fixture_library_id, 
                                          fixture.channel_mode, fixture.id, 
                                          fixture.display_name, 
                                          fixture.dmx_start_address)
        self._get_fixtures()
        self._notify_fixtures_changed()
    
    @pyqtSlot(int)
    def remove_fixture_handler(self, index) -> None:
        self._fixture_manager.remove_fixture(index)  # remove the fixture from the json file with fixture manager
        self._selected_fixtures = {}  # reset the selected fixtures
        self._get_fixtures()  # reload fixtures
        self._notify_fixtures_changed()  # notify the view
        
    @pyqtSlot(int, list)  
    def add_fixture_to_stage_view_handler(self, index: int, coordinates: list) -> None:
        self._fixture_manager.add_fixture_to_stage_view(index, coordinates) # add fixture to stage_view databas
        self._fixture_manager.change_fixture_in_stage_view_status(index, True)  # change the status of the fixture in the fixture_patch database
        self._get_fixtures()  # reload fixtures
        self._notify_fixtures_changed()  # notify the view
    
    @pyqtSlot()
    def update_fixture_patch_handler(self) -> None:
        self._get_fixtures()  # reload fixtures
        self._notify_fixtures_changed()  # notify the view
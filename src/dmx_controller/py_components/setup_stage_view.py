from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from py_managers.fixture_manager import FixtureManager
from py_managers.dmx_data_generation_manager import DmxDataGenerationManager

class SetupStageView(QObject):

    stage_view_fixtures_list_lenght_updated: pyqtSignal = pyqtSignal(int)
    all_fixtures_in_stage_view_updated: pyqtSignal = pyqtSignal(list)
    dmx_data_updated: pyqtSignal = pyqtSignal(dict)
    
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self._fixture_manager: FixtureManager = FixtureManager()
        self._dmx_data_generation_manager: DmxDataGenerationManager = DmxDataGenerationManager()
        self.check_stage_view_fixtures_list_lenght_handler()

    @pyqtSlot()
    def check_stage_view_fixtures_list_lenght_handler(self):
        lenght = self._fixture_manager.count_stage_view_fixtures()
        self.stage_view_fixtures_list_lenght_updated.emit(lenght)

    @pyqtSlot(int, list)
    def change_fixture_stage_view_coordinates_handler(self, fixture_index, coordinates: list):
        self._fixture_manager.change_fixtures_stage_view_coordinates(
            fixture_index, coordinates)

    @pyqtSlot()
    def get_all_fixtures_in_stage_view_handler(self):
        all_fixtures_in_stage_view = self._fixture_manager.list_all_fixtures_in_stage_view()
        self.all_fixtures_in_stage_view_updated.emit(all_fixtures_in_stage_view)

    @pyqtSlot(int)
    def delete_fixture_from_stage_view_handler(self, fixture_index: int):
        self._fixture_manager.delete_fixture_from_stage_view(fixture_index)

    @pyqtSlot(int)
    def add_fixture_to_selection_handler(self, fixture_index: int):
        self._fixture_manager.add_fixture_to_selection(fixture_index)
        
    @pyqtSlot(int, int, int, int, int)
    def set_fixture_color_handler(self, fixture_index: int, red: int, green: int, blue: int, dimmer: int):
        white = 0
        self._dmx_data_generation_manager.change_temp_cue_drgbw_fixture_color(fixture_index, dimmer, red, green, blue, white)
    
    @pyqtSlot()
    def reset_temp_cue_data_handler(self):
        self._dmx_data_generation_manager.reset_temp_cue_data()
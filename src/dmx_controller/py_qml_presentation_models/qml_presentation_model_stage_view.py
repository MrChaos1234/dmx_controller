from PyQt5.QtCore import Qt, QObject, QAbstractListModel, QModelIndex, pyqtSignal, pyqtSlot, pyqtProperty

from py_qml_presentation_models.qml_presentation_model_fixture import FixtureQmlPresentationModel

class StageViewQmlPresentationModel(QObject):
    add_fixture_to_stage_view_requested: pyqtSignal = pyqtSignal(int, list)
    add_fixture_to_stage_view_wish_requested: pyqtSignal = pyqtSignal()
    change_fixture_stage_view_coordinates_requested: pyqtSignal = pyqtSignal(
        int, list)

    stage_view_current_fixture_index: pyqtSignal = pyqtSignal(int)

    get_all_fixtures_in_stage_view_requested:pyqtSignal = pyqtSignal()
    delete_fixture_from_stage_view_requested: pyqtSignal = pyqtSignal(int)
    
    add_fixture_to_selection_requested: pyqtSignal = pyqtSignal(int)
    
    set_fixture_color_requested: pyqtSignal = pyqtSignal(int, int, int, int, int)
    
    reset_temp_cue_data_requested: pyqtSignal = pyqtSignal()
    
    _lenght: int

    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self._lenght: int = 0
        self._all_fixtures_in_stage_view: list = []
        self._selected_fixtures: list = []
        self._dmx_data: dict = {}
        
    def setup(self):
        self.reset_temp_cue_data_requested.emit()
            
    @pyqtSlot(int)
    def stage_view_fixtures_list_lenght_updated_handler(self, lenght: int):
        print("lenght: " + str(lenght))
        self._lenght: int = lenght

    @pyqtSlot(list)
    def all_fixtures_in_stage_view_updated_handler(self, fixtures_in_stage_view: list):
        self._all_fixtures_in_stage_view: list = fixtures_in_stage_view
        

    @pyqtSlot(int)
    def add_fixture_to_stage_view(self, fixture_index: int) -> None:
        print("Add fixture to stage view")
        print("fixture index: " + str(fixture_index))
        coordinates = self.coordinates

        self.stage_view_current_fixture_index.emit(fixture_index)
        self.add_fixture_to_stage_view_requested.emit(
            fixture_index, coordinates)

    @pyqtSlot(int, int)
    def add_fixture_to_stage_view_wish(self, x: int, y: int) -> None:
        print("want to add fixture to stage view now")
        print("coordinates: " + str(x) + " " + str(y))

        self.coordinates = [x, y]

        self.add_fixture_to_stage_view_wish_requested.emit()

    @pyqtSlot(int, int, int)
    def change_fixture_stage_view_coordinates(self, fixture_index: int, x: int, y: int):
        print("want to change fixtures position to: " + str(x) + " and " + str(y))
        coordinates = [x, y]
        self.change_fixture_stage_view_coordinates_requested.emit(
            fixture_index, coordinates)

    @pyqtSlot(int, result=str)
    def get_matching_symbol_number(self, fixture_library_id):
        symbol_path: str = f"../data/fixture_library/symbols/{str(fixture_library_id)}.png"
        return symbol_path
    
    @pyqtSlot(result=list)
    def get_all_fixtures_in_stage_view(self):
        print("get all fixtures in stage view")
        self.get_all_fixtures_in_stage_view_requested.emit()
        return self._all_fixtures_in_stage_view

    @pyqtSlot(int, int, int, result=bool)
    def check_if_fixture_is_in_deleting_area(self, fixture_id, x, y):
        deleting_area_x = [-10, 100]
        deleting_area_y = [790, 890]
        
        # check if x and y are in deleting area
        if x >= deleting_area_x[0] and x <= deleting_area_x[1] and y >= deleting_area_y[0] and y <= deleting_area_y[1]:
            print("Fixture is in deleting area")
            # make sure the user really want to delete the fixture
            return True
        else:
            return False
        
    @pyqtSlot(int)
    def delete_fixture_from_stage_view(self, fixture_id):
        print("delete fixture from stage view")
        self.delete_fixture_from_stage_view_requested.emit(fixture_id)
        
    @pyqtSlot(int)
    def add_fixture_to_selection(self, fixture_id):
        print("add fixture to selection")
        if fixture_id in self._selected_fixtures:
            print("fixture already in selection")
        else:
            self._selected_fixtures.append(fixture_id)
    
    @pyqtSlot(int)
    def remove_fixture_from_selection(self, fixture_id):
        print("remove fixture to selection")
        if fixture_id in self._selected_fixtures:
            self._selected_fixtures.remove(fixture_id)
        else:
            print("fixture not in selection")
        
    @pyqtSlot(result=list)
    def get_selected_fixtures(self):
        print("get selected fixtures")
        return self._selected_fixtures

    @pyqtSlot()
    def clear_selected_fixtures_list(self):
        print("clear selected fixtures list")
        self._selected_fixtures = []
        
    @pyqtSlot(int, int, int, int, int)
    def set_fixture_color(self, fixture_id, r, g, b, dimmer):
        print("set fixture color")
        print("fixture id: " + str(fixture_id) + " r: " + str(r) + " g: " + str(g) + " b: " + str(b) + "dimmer" + str(dimmer))
        
        # use dmx data generation mamager to add color to dmx data file
        self.set_fixture_color_requested.emit(fixture_id, r, g, b, dimmer)
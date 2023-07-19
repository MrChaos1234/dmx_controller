from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from threads.i2c_thread import I2cThread

from py_qml_presentation_models.qml_presentation_model_cue_list import CueListQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_artnet_output import ArtnetOutputQmlPresentationModel

class XButtons(QObject):

    # signal to emit when a key is pressed
    key_pressed: pyqtSignal = pyqtSignal(int)
    # signal to emit when a key is released
    key_released: pyqtSignal = pyqtSignal(int)

    _i2c_thread: I2cThread

    page_up_requested: pyqtSignal = pyqtSignal()
    page_down_requested: pyqtSignal = pyqtSignal()
    
    def __init__(self,
                 i2c_thread: I2cThread,
                 qml_presentation_model_cue_list: CueListQmlPresentationModel,
                 qml_presentation_model_artnet_output: ArtnetOutputQmlPresentationModel,
                 parent: QObject = None):
        super().__init__(parent)
        self._i2c_thread = i2c_thread
        
        self._qml_presentation_model_cue_list = qml_presentation_model_cue_list
        self._qml_presentation_model_artnet_output = qml_presentation_model_artnet_output
        
    @pyqtSlot()
    def setup(self) -> None:
        self._i2c_thread.x_key_pressed.connect(self.x_key_pressed_handler)
        self._i2c_thread.x_key_released.connect(self.x_key_released_handler)

    @pyqtSlot(int)
    def x_key_pressed_handler(self, key_number: int) -> None:
        # self.key_pressed.emit(key_number)
        # print("x key pressed: " + str(key_number))
        
        # if key number is 30 or 31, its the page up/down button
        if key_number == 30:
            self.page_up_requested.emit()
            return
        elif key_number == 31:
            self.page_down_requested.emit()
            return
        
                
        try:
            cue_id = int(self._qml_presentation_model_cue_list.find_tile_cue_relation(key_number - 1))
        except ValueError:
            cue_id = 0
        
        if key_number <= 10:
            reaction_mode = self._qml_presentation_model_cue_list.get_button_grid_reaction_mode_1()
        else:
            reaction_mode = self._qml_presentation_model_cue_list.get_button_grid_reaction_mode_2()

        if reaction_mode:
            # if in reaction mode, the cue has to be pressed to start and pressed again to be cleared
            if not self._qml_presentation_model_cue_list.get_button_state(key_number - 1):
                # find out cue id of the button
                self._qml_presentation_model_artnet_output.execute_cue(cue_id)  # execute the cue
                self._qml_presentation_model_cue_list.set_button_state(key_number - 1, True)  
                for i in range(0, 20):
                    if i != key_number - 1:
                        try:
                            self._qml_presentation_model_cue_list.set_button_state(i, False)
                        except ValueError:
                            pass
                        
            else:
                print("else")
                self._qml_presentation_model_artnet_output.clear_cue(cue_id)  # clear the cue
                self._qml_presentation_model_cue_list.set_button_state(key_number - 1, False)
        else:
            self._qml_presentation_model_artnet_output.execute_cue(cue_id)  # clear the cue
                  
    @pyqtSlot(int)
    def x_key_released_handler(self, key_number: int) -> None:
        # self.key_released.emit(key_number)
        
         # if key number is 30 or 31, its the page up/down button
        if key_number == 30:
            return
        elif key_number == 31:
            return
        
        try:
            cue_id = int(self._qml_presentation_model_cue_list.find_tile_cue_relation(key_number - 1))
        except ValueError:
            cue_id = 0
        
        if key_number <= 10:
            reaction_mode = self._qml_presentation_model_cue_list.get_button_grid_reaction_mode_1()
        else:
            reaction_mode = self._qml_presentation_model_cue_list.get_button_grid_reaction_mode_2()
        
        if reaction_mode:
            # do nothing
            pass
        else:
            self._qml_presentation_model_artnet_output.clear_cue(cue_id)  # clear the cue

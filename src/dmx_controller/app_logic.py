import RPi.GPIO as GPIO

from py_drivers.driver_rotary_encoder import GpioBasedRotaryEncoderDriver

from py_components.double_speed_rotary_encoder import DoubleSpeedRotaryEncoder
from py_components.rotary_encoder import RotaryEncoder

from py_qml_presentation_models.double_speed_rotary_encoder_qml_presentation_model import DoubleSpeedRotaryEncoderQmlPresentationModel
from py_qml_presentation_models.rotary_encoder_qml_presentation_model import RotaryEncoderQmlPresentationModel

from py_qml_presentation_models.qml_presentation_model_fixture import FixtureQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_dmx_fixture_patch import DmxFixturePatchQmlPresentationModel

from py_qml_presentation_models.qml_presentation_model_cue import CueQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_cue_list import CueListQmlPresentationModel

from py_qml_presentation_models.qml_presentation_model_stage_view import StageViewQmlPresentationModel
from py_components.setup_stage_view import SetupStageView

from py_components.dmx_fixture_patch import DmxFixturePatch
from py_components.cue_list import CueList

from py_managers.fixture_manager import FixtureManager
from py_managers.cue_manager import CueManager

from py_qml_presentation_models.qml_presentation_model_fixture_library import FixtureLibraryQmlPresentationModel
from py_components.fixture_library import FixtureLibrary

from py_qml_presentation_models.qml_presentation_model_color_picker import ColorPickerQmlPresentationModel
from py_components.color_picker import ColorPicker

from py_qml_presentation_models.qml_presentation_model_dmx_list import DmxListQmlPresentationModel
from py_components.dmx_list import DmxList

from py_qml_presentation_models.qml_presentation_model_fader import FaderQmlPresentationModel
from py_components.fader_controller_connection import FaderControllerConnection
from py_components.fader import Fader

from py_managers.artnet_manager import ArtnetManager

from py_qml_presentation_models.qml_presentation_model_artnet_output import ArtnetOutputQmlPresentationModel
from py_components.artnet_output import ArtnetOutput

from py_managers.dmx_data_generation_manager import DmxDataGenerationManager

from py_qml_presentation_models.qml_presentation_model_x_buttons import XButtonsQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_k_keypad import KKeypadQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_hardware_led import HardwareLedQmlPresentationModel

from py_components.x_buttons import XButtons
from threads.i2c_thread import I2cThread
from py_components.k_keypad import KKeypad
from py_components.hardware_led import HardwareLed
from py_drivers.driver_x_buttons import XButtonsDriver
from py_drivers.driver_k_keypad import I2cKeypadDriver
from py_drivers.driver_led import I2cLedDriver

from py_qml_presentation_models.qml_presentation_model_effects import EffectsQmlPresentationModel
from py_components.effects import Effects
from py_managers.effects_manager import EffectsManager

from py_components.fader_page import FaderPage


class AppLogic():
    # number of GPIO (not pin number!) for signal A of rotary encoder 0
    GPIO_NUMBER_ROTARY_ENCODER_A_0: int = 17
    # number of GPIO (not pin number!) for signal B of rotary encoder 0
    GPIO_NUMBER_ROTARY_ENCODER_B_0: int = 27
    # number of GPIO (not pin number!) for signal of pushbutton of rotary encoder 0
    GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_0: int = 22

    # number of GPIO (not pin number!) for signal A of rotary encoder 1
    GPIO_NUMBER_ROTARY_ENCODER_A_1: int = 5
    # number of GPIO (not pin number!) for signal B of rotary encoder 1
    GPIO_NUMBER_ROTARY_ENCODER_B_1: int = 6
    # number of GPIO (not pin number!) for signal of pushbutton of rotary encoder 1
    GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_1: int = 11

    # number of GPIO (not pin number!) for signal A of rotary encoder 2
    GPIO_NUMBER_ROTARY_ENCODER_A_2: int = 18
    # number of GPIO (not pin number!) for signal B of rotary encoder 2
    GPIO_NUMBER_ROTARY_ENCODER_B_2: int = 23
    # number of GPIO (not pin number!) for signal of pushbutton of rotary encoder 2
    GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_2: int = 24

    # number of GPIO (not pin number!) for signal A of rotary encoder 3
    GPIO_NUMBER_ROTARY_ENCODER_A_3: int = 25
    # number of GPIO (not pin number!) for signal B of rotary encoder 3
    GPIO_NUMBER_ROTARY_ENCODER_B_3: int = 26
    # number of GPIO (not pin number!) for signal of pushbutton of rotary encoder 3
    GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_3: int = 12

    # the rotary encoder hardware instance, that is used to realize the double speed rotary encoder instance
    _gpio_based_rotary_encoder_driver_0: GpioBasedRotaryEncoderDriver
    # the rotary encoder hardware instance, that is used to realize the double speed rotary encoder instance
    _gpio_based_rotary_encoder_driver_1: GpioBasedRotaryEncoderDriver
    # the rotary encoder hardware instance, that is used to realize the double speed rotary encoder instance
    _gpio_based_rotary_encoder_driver_2: GpioBasedRotaryEncoderDriver
    # the rotary encoder hardware instance, that is used to realize the double speed rotary encoder instance
    _gpio_based_rotary_encoder_driver_3: GpioBasedRotaryEncoderDriver
    # the double speed rotary encoder instance
    _double_speed_rotary_encoder_0: DoubleSpeedRotaryEncoder
    # the double speed rotary encoder instance
    _double_speed_rotary_encoder_1: DoubleSpeedRotaryEncoder
    # the double speed rotary encoder instance
    _double_speed_rotary_encoder_2: DoubleSpeedRotaryEncoder
    # the double speed rotary encoder instance
    _double_speed_rotary_encoder_3: DoubleSpeedRotaryEncoder

    # the QML presentation model representing the double speed rotary encoder instance
    _double_speed_rotary_encoder_qml_presentation_model_0: DoubleSpeedRotaryEncoderQmlPresentationModel
    # the QML presentation model representing the double speed rotary encoder instance
    _double_speed_rotary_encoder_qml_presentation_model_1: DoubleSpeedRotaryEncoderQmlPresentationModel
    # the QML presentation model representing the double speed rotary encoder instance
    _double_speed_rotary_encoder_qml_presentation_model_2: DoubleSpeedRotaryEncoderQmlPresentationModel
    # the QML presentation model representing the double speed rotary encoder instance
    _double_speed_rotary_encoder_qml_presentation_model_3: DoubleSpeedRotaryEncoderQmlPresentationModel

    _fixture_qml_presentation_models: list[FixtureQmlPresentationModel]
    _fixtures_qml_presentation_model: DmxFixturePatchQmlPresentationModel

    _stage_view_qml_presentation_model: StageViewQmlPresentationModel
    _setup_stage_view: SetupStageView

    _dmx_fixture_patch: DmxFixturePatch
    _cue_list: CueList

    _fixture_manager: FixtureManager
    _cue_manager: CueManager

    _fixture_library_qml_presentation_model: FixtureLibraryQmlPresentationModel
    _fixture_library: FixtureLibrary

    _cues_qml_presentation_models: list[CueQmlPresentationModel]
    _cue_qml_presentation_model: CueListQmlPresentationModel

    # the QML presentation model representing the RGB color picker instance
    _rgb_color_picker_qml_presentation_model: ColorPickerQmlPresentationModel
    _rgb_color_picker: ColorPicker  # the RGB color picker instance

    _dmx_list_qml_presentations_model: DmxListQmlPresentationModel

    _qml_fader_qml_presentation_model: FaderQmlPresentationModel
    _driver_fader_controller_connection: FaderControllerConnection

    _fader_0: Fader
    _fader_1: Fader
    _fader_2: Fader
    _fader_3: Fader

    _artnet_manager: ArtnetManager

    _artnet_output_qml_presentation_model: ArtnetOutputQmlPresentationModel
    _artnet_output: ArtnetOutput

    _dmx_generation_manager: DmxDataGenerationManager

    _x_buttons_qml_presentation_model: XButtonsQmlPresentationModel
    _i2c_connection: I2cThread
    
    _effects_qml_presentations_model: EffectsQmlPresentationModel

    _x_buttons: XButtons
    
    def __init__(self, double_speed_rotary_encoder_qml_presentation_model_0: DoubleSpeedRotaryEncoderQmlPresentationModel,
                 double_speed_rotary_encoder_qml_presentation_model_1: DoubleSpeedRotaryEncoderQmlPresentationModel,
                 double_speed_rotary_encoder_qml_presentation_model_2: DoubleSpeedRotaryEncoderQmlPresentationModel,
                 double_speed_rotary_encoder_qml_presentation_model_3: DoubleSpeedRotaryEncoderQmlPresentationModel,
                 fixture_qml_presentation_models: list[FixtureQmlPresentationModel],
                 fixtures_qml_presentation_model: DmxFixturePatchQmlPresentationModel,
                 fixture_library_qml_presentation_model: FixtureLibraryQmlPresentationModel,
                 color_picker_qml_presentation_model: ColorPickerQmlPresentationModel,
                 dmx_list_qml_presentations_model: DmxListQmlPresentationModel,
                 stage_view_qml_presentation_model: StageViewQmlPresentationModel,
                 setup_stage_view: SetupStageView,
                 cue_list_qml_presentation_model: CueListQmlPresentationModel,
                 cues_list_qml_presentation_models: list[CueQmlPresentationModel],
                 qml_fader_qml_presentation_model: FaderQmlPresentationModel,
                 artnet_output_qml_presentation_model: ArtnetOutputQmlPresentationModel,
                 x_buttons_qml_presentation_model: XButtonsQmlPresentationModel,
                 effects_qml_presentations_model: EffectsQmlPresentationModel,
                 debouncing_external_timer_frequency: int):

        # double speed rotary encoder 0
        self._double_speed_rotary_encoder_qml_presentation_model_0 = double_speed_rotary_encoder_qml_presentation_model_0
        self._gpio_based_rotary_encoder_driver_0 = GpioBasedRotaryEncoderDriver(self.GPIO_NUMBER_ROTARY_ENCODER_A_0,
                                                                                self.GPIO_NUMBER_ROTARY_ENCODER_B_0,
                                                                                self.GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_0,
                                                                                debouncing_external_timer_frequency)
        self._double_speed_rotary_encoder_0 = DoubleSpeedRotaryEncoder(
            self._gpio_based_rotary_encoder_driver_0)
        self._double_speed_rotary_encoder_0.is_in_double_speed_mode_changed.connect(
            self._double_speed_rotary_encoder_qml_presentation_model_0.is_in_double_speed_mode_changed)
        self._double_speed_rotary_encoder_0.position_changed.connect(
            self._double_speed_rotary_encoder_qml_presentation_model_0.position_changed)
        self._double_speed_rotary_encoder_qml_presentation_model_0.is_in_double_speed_mode_toggled.connect(
            self._double_speed_rotary_encoder_0.toggle_is_in_double_speed_mode)

        # double speed rotary encoder 1
        self._double_speed_rotary_encoder_qml_presentation_model_1 = double_speed_rotary_encoder_qml_presentation_model_1
        self._gpio_based_rotary_encoder_driver_1 = GpioBasedRotaryEncoderDriver(self.GPIO_NUMBER_ROTARY_ENCODER_A_1,
                                                                                self.GPIO_NUMBER_ROTARY_ENCODER_B_1,
                                                                                self.GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_1,
                                                                                debouncing_external_timer_frequency)
        self._double_speed_rotary_encoder_1 = DoubleSpeedRotaryEncoder(
            self._gpio_based_rotary_encoder_driver_1)
        self._double_speed_rotary_encoder_1.is_in_double_speed_mode_changed.connect(
            self._double_speed_rotary_encoder_qml_presentation_model_1.is_in_double_speed_mode_changed)
        self._double_speed_rotary_encoder_1.position_changed.connect(
            self._double_speed_rotary_encoder_qml_presentation_model_1.position_changed)
        self._double_speed_rotary_encoder_qml_presentation_model_1.is_in_double_speed_mode_toggled.connect(
            self._double_speed_rotary_encoder_1.toggle_is_in_double_speed_mode)

        # double speed rotary encoder 2
        self._double_speed_rotary_encoder_qml_presentation_model_2 = double_speed_rotary_encoder_qml_presentation_model_2
        self._gpio_based_rotary_encoder_driver_2 = GpioBasedRotaryEncoderDriver(self.GPIO_NUMBER_ROTARY_ENCODER_A_2,
                                                                                self.GPIO_NUMBER_ROTARY_ENCODER_B_2,
                                                                                self.GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_2,
                                                                                debouncing_external_timer_frequency)
        self._double_speed_rotary_encoder_2 = DoubleSpeedRotaryEncoder(
            self._gpio_based_rotary_encoder_driver_2)
        self._double_speed_rotary_encoder_2.is_in_double_speed_mode_changed.connect(
            self._double_speed_rotary_encoder_qml_presentation_model_2.is_in_double_speed_mode_changed)
        self._double_speed_rotary_encoder_2.position_changed.connect(
            self._double_speed_rotary_encoder_qml_presentation_model_2.position_changed)
        self._double_speed_rotary_encoder_qml_presentation_model_2.is_in_double_speed_mode_toggled.connect(
            self._double_speed_rotary_encoder_2.toggle_is_in_double_speed_mode)

        # double speed rotary encoder 3
        self._double_speed_rotary_encoder_qml_presentation_model_3 = double_speed_rotary_encoder_qml_presentation_model_3
        self._gpio_based_rotary_encoder_driver_3 = GpioBasedRotaryEncoderDriver(self.GPIO_NUMBER_ROTARY_ENCODER_A_3,
                                                                                self.GPIO_NUMBER_ROTARY_ENCODER_B_3,
                                                                                self.GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_3,
                                                                                debouncing_external_timer_frequency)
        self._double_speed_rotary_encoder_3 = DoubleSpeedRotaryEncoder(
            self._gpio_based_rotary_encoder_driver_3)
        self._double_speed_rotary_encoder_3.is_in_double_speed_mode_changed.connect(
            self._double_speed_rotary_encoder_qml_presentation_model_3.is_in_double_speed_mode_changed)
        self._double_speed_rotary_encoder_3.position_changed.connect(
            self._double_speed_rotary_encoder_qml_presentation_model_3.position_changed)
        self._double_speed_rotary_encoder_qml_presentation_model_3.is_in_double_speed_mode_toggled.connect(
            self._double_speed_rotary_encoder_3.toggle_is_in_double_speed_mode)

        # Fixture Patch
        self._fixture_qml_presentation_models = fixture_qml_presentation_models
        self._fixtures_qml_presentation_model = fixtures_qml_presentation_model
        self._fixture_manager = FixtureManager()
        self._dmx_fixture_patch = DmxFixturePatch(self._fixture_manager)
        self._dmx_fixture_patch.fixtures_changed.connect(
            self._fixtures_qml_presentation_model.fixtures_changed)
        self._fixtures_qml_presentation_model.change_fixture_selected_status.connect(
            self._dmx_fixture_patch.change_fixture_selected_status_handler)
        self._fixtures_qml_presentation_model.add_fixture_requested.connect(
            self._dmx_fixture_patch.add_fixture_handler)
        self._fixtures_qml_presentation_model.remove_fixture_requested.connect(
            self._dmx_fixture_patch.remove_fixture_handler)
        self._fixtures_qml_presentation_model.update_fixture_patch_requested.connect(
            self._dmx_fixture_patch.update_fixture_patch_handler)

        # Fixture Library
        self._fixture_library_qml_presentation_model = fixture_library_qml_presentation_model
        self._fixture_library = FixtureLibrary(self._fixture_manager)
        self._fixture_library.library_fixtures_changed.connect(
            self._fixture_library_qml_presentation_model.library_fixtures_changed)

        # Stage View
        self._stage_view_qml_presentation_model = stage_view_qml_presentation_model
        self._setup_stage_view = setup_stage_view
        self._stage_view_qml_presentation_model.add_fixture_to_stage_view_requested.connect(self._dmx_fixture_patch.add_fixture_to_stage_view_handler)
        self._stage_view_qml_presentation_model.change_fixture_stage_view_coordinates_requested.connect(self._setup_stage_view.change_fixture_stage_view_coordinates_handler)
        self._stage_view_qml_presentation_model.get_all_fixtures_in_stage_view_requested.connect(self._setup_stage_view.get_all_fixtures_in_stage_view_handler)
        self._stage_view_qml_presentation_model.delete_fixture_from_stage_view_requested.connect(self._setup_stage_view.delete_fixture_from_stage_view_handler)
        self._stage_view_qml_presentation_model.add_fixture_to_selection_requested.connect(self._setup_stage_view.add_fixture_to_selection_handler)
        self._stage_view_qml_presentation_model.set_fixture_color_requested.connect(self._setup_stage_view.set_fixture_color_handler)
        self._stage_view_qml_presentation_model.reset_temp_cue_data_requested.connect(self._setup_stage_view.reset_temp_cue_data_handler)
        
        self._setup_stage_view.stage_view_fixtures_list_lenght_updated.connect(self._stage_view_qml_presentation_model.stage_view_fixtures_list_lenght_updated_handler)
        self._setup_stage_view.all_fixtures_in_stage_view_updated.connect(self._stage_view_qml_presentation_model.all_fixtures_in_stage_view_updated_handler)

        

        # Cue List
        self._cues_qml_presentation_models = cues_list_qml_presentation_models
        self._cue_qml_presentation_model = cue_list_qml_presentation_model
        self._cue_manager = CueManager()
        self._cue_list = CueList(self._cue_manager)
        self._cue_list.cues_changed.connect(
            self._cue_qml_presentation_model.cues_changed)
        self._cue_list.button_grid_view_changed.connect(
            self._cue_qml_presentation_model.button_grid_view_changed_handler)
        self._cue_list.cue_list_updated.connect(
            self._cue_qml_presentation_model.cue_list_updated_handler)

        self._cue_qml_presentation_model.change_cue_selected_status.connect(
            self._cue_list.change_cue_selected_status_handler)
        self._cue_qml_presentation_model.add_cue_requested.connect(
            self._cue_list.add_cue_handler)
        self._cue_qml_presentation_model.remove_cue_requested.connect(
            self._cue_list.remove_cue_handler)
        self._cue_qml_presentation_model.update_cue_list_requested.connect(
            self._cue_list.update_cue_list_handler)
        self._cue_qml_presentation_model.update_button_grid_view_requested.connect(
            self._cue_list.update_button_grid_view_handler)
        self._cue_qml_presentation_model.add_tile_cue_relation_requested.connect(
            self._cue_list.add_tile_cue_relation_handler)
        self._cue_qml_presentation_model.get_cue_list_requested.connect(
            self._cue_list.get_cue_list_handler)
        self._cue_qml_presentation_model.remove_tile_cue_relation_requested.connect(
            self._cue_list.remove_tile_cue_relation_handler)

        # RGB color picker
        self._color_picker_qml_presentation_model = color_picker_qml_presentation_model
        self._rgb_color_picker = ColorPicker(self._double_speed_rotary_encoder_0,
                                             self._double_speed_rotary_encoder_1,
                                             self._double_speed_rotary_encoder_2,
                                             self._double_speed_rotary_encoder_3)
        # connect signals of RGB color picker instance with slots of belonging QML presentation model (in both directions!)
        self._rgb_color_picker.r_changed.connect(
            self._color_picker_qml_presentation_model.r_changed)
        self._rgb_color_picker.g_changed.connect(
            self._color_picker_qml_presentation_model.g_changed)
        self._rgb_color_picker.b_changed.connect(
            self._color_picker_qml_presentation_model.b_changed)
        self._rgb_color_picker.dimmer_changed.connect(
            self._color_picker_qml_presentation_model.dimmer_changed)
        self._color_picker_qml_presentation_model.mixed_color_updated.connect(
            self._rgb_color_picker.change_mixed_color)

        self._dmx_list_qml_presentations_model = dmx_list_qml_presentations_model
        self._fixture_manager = FixtureManager()
        self._dmx_list: DmxList = DmxList(self._fixture_manager)
        self._dmx_list.dmx_data_changed.connect(
            self._dmx_list_qml_presentations_model.list_updated)
        
        # Fader
        self._qml_fader_qml_presentation_model = qml_fader_qml_presentation_model     

        # Fader Controller Connection
        self._fader_controller_connection = FaderControllerConnection()
        self._qml_fader_qml_presentation_model.set_faders_count_0_triggered.connect(
            self._fader_controller_connection.set_faders_count)
        self._qml_fader_qml_presentation_model.set_max_motor_stop_timeout_counter_0_triggered.connect(
            self._fader_controller_connection.set_max_motor_stop_timeout_counter)
        self._qml_fader_qml_presentation_model.setup_connection_0_triggered.connect(
            self._fader_controller_connection.setup)
        self._qml_fader_qml_presentation_model.cleanup_connection_0_triggered.connect(
            self._fader_controller_connection.cleanup)
        
        
        # fader page init
        self._fader_page = FaderPage(self._qml_fader_qml_presentation_model)
                
        # fader 0
        self._fader_0 = Fader(self._fader_controller_connection, 0, 0, 1023, 0, 1023)
        self._fader_0.position_changed.connect(self._qml_fader_qml_presentation_model.position_fader0_changed)
        self._fader_0.position_changed.connect(self._fader_page.faderPosition0_updated_handler)
        self._qml_fader_qml_presentation_model.set_position_set_value_0_triggered.connect(self._fader_0.position_fader)
        # fader 1
        self._fader_1 = Fader(self._fader_controller_connection, 1, 0, 1023, 0, 1023)
        self._fader_1.position_changed.connect(self._qml_fader_qml_presentation_model.position_fader1_changed)
        self._fader_1.position_changed.connect(self._fader_page.faderPosition1_updated_handler)
        self._qml_fader_qml_presentation_model.set_position_set_value_1_triggered.connect(self._fader_1.position_fader)
        # fader 2
        self._fader_2 = Fader(self._fader_controller_connection, 2, 0, 1023, 0, 1023)
        self._fader_2.position_changed.connect(self._qml_fader_qml_presentation_model.position_fader2_changed)
        self._fader_2.position_changed.connect(self._fader_page.faderPosition2_updated_handler)
        self._qml_fader_qml_presentation_model.set_position_set_value_2_triggered.connect(self._fader_2.position_fader)
        # fader 3
        self._fader_3 = Fader(self._fader_controller_connection, 3, 0, 1023, 0, 1023)
        self._fader_3.position_changed.connect(self._qml_fader_qml_presentation_model.position_fader3_changed)
        self._fader_3.position_changed.connect(self._fader_page.faderPosition3_updated_handler)
        self._qml_fader_qml_presentation_model.set_position_set_value_3_triggered.connect(self._fader_3.position_fader)
        
        
        # Fader Page
        self._fader_page.active_page_id_changed.connect(self._qml_fader_qml_presentation_model.active_page_id_changed_handler)
        self._qml_fader_qml_presentation_model.fader_page_position_changed.connect(self._fader_page.fader_page_position_changed_handler)
        
        self._fader_page.set_fader_0_to_position.connect(self._fader_0.position_fader)
        self._fader_page.set_fader_1_to_position.connect(self._fader_1.position_fader)
        self._fader_page.set_fader_2_to_position.connect(self._fader_2.position_fader)
        self._fader_page.set_fader_3_to_position.connect(self._fader_3.position_fader)
        
        
        
        # DMX Generation
        self._dmx_generation_manager = DmxDataGenerationManager()

                
        # Artnet Output
        self._artnet_manager = ArtnetManager(512)
        self._artnet_output = ArtnetOutput(self._artnet_manager, self._cue_manager, self._dmx_generation_manager)
        self._artnet_output_qml_presentation_model = artnet_output_qml_presentation_model

        self._artnet_output_qml_presentation_model.execute_cue_requested.connect(self._artnet_output.execute_cue_handler)
        self._artnet_output_qml_presentation_model.clear_cue_requested.connect(self._artnet_output.clear_cue_handler)
        self._artnet_output_qml_presentation_model.clear_output_requested.connect(self._artnet_output.clear_output_handler)
        
        self._cue_qml_presentation_model.updated.connect(self._artnet_output.update_cue_list)
        
        # Effects Manager (needs to be defined here because its user via siganl)
        self._effects_manager = EffectsManager(self._artnet_manager, self._artnet_output)
        self._effects = Effects(self._effects_manager)
        
        self._cue_qml_presentation_model.block_unblock_faders.connect(self._fader_page.block_unblock_faders_handler)
        self._effects.block_unblock_faders.connect(self._fader_page.block_unblock_faders_handler)
        
        # Artnet again
        self._artnet_output.stop_effect_requested.connect(self._effects.stop_effect_handler)
        
        #x Buttons
        self._i2c_connection: I2cThread = I2cThread() # Create an Object of the I2cThread class
        self.k_keypad: KKeypad = KKeypad(self._i2c_connection) # Create an Object of the KKeypad class
        hardware_leds: HardwareLed = HardwareLed(self._i2c_connection) # Create an Object of the KKeypad class
        self.x_buttons: XButtons = XButtons(self._i2c_connection, self._cue_qml_presentation_model, self._artnet_output_qml_presentation_model) # Create an Object of the XButtons class
        
        # Create an Object of the KKeypadQmlPresentationModel class
        k_keypad_qml_presentation_model: KKeypadQmlPresentationModel = KKeypadQmlPresentationModel()
        # Create an Object of the HardwareLedQmlPresentationModel class
        hardware_leds_qml_presentation_model: HardwareLedQmlPresentationModel = HardwareLedQmlPresentationModel()
        # Create an Object of the XButtonsQmlPresentationModel class
        self._x_buttons_qml_presentation_model: XButtonsQmlPresentationModel = x_buttons_qml_presentation_model

        # Connect the key_pressed signal of the KKeypad class to the key_pressed_handler slot of the KKeypadQmlPresentationModel class
        self.k_keypad.key_pressed.connect(k_keypad_qml_presentation_model.key_pressed_handler)
        # Connect the key_released signal of the KKeypad class to the key_released_handler slot of the KKeypadQmlPresentationModel class
        self.k_keypad.key_released.connect(k_keypad_qml_presentation_model.key_released_handler)

        self.k_keypad.clear_output_key.connect(self._artnet_output.clear_output_handler)

        self.k_keypad.start_effect.connect(self._effects.start_effect_handler)
        self.k_keypad.stop_effect.connect(self._effects.stop_effect_handler)
        
        # Connect the x_key_pressed signal of the XButtons class to the key_pressed_handler slot of the XButtonsQmlPresentationModel class
        self.x_buttons.key_pressed.connect(self._x_buttons_qml_presentation_model.x_key_pressed_handler)
        # Connect the x_key_released signal of the XButtons class to the key_released_handler slot of the XButtonsQmlPresentationModel class
        self.x_buttons.key_released.connect(self._x_buttons_qml_presentation_model.x_key_released_handler)

        # Connect the hardware_led_color_change signal of the HardwareLedQmlPresentationModel class to the change_led_color slot of the Led class
        hardware_leds_qml_presentation_model.hardware_led_color_change.connect(
            hardware_leds.change_led_color)

        # Connect the led_color_change signal of the Led class to the led_color_change_handler slot of the I2cThread class
        hardware_leds.hardware_led_color_change.connect(
            self._i2c_connection.led_color_change_handler)
        
        self.x_buttons.page_down_requested.connect(self._fader_page.page_down_handler)
        self.x_buttons.page_up_requested.connect(self._fader_page.page_up_handler)
        
        # Effects
        self._effects_qml_presentations_model = effects_qml_presentations_model
        self._effects_qml_presentations_model.start_effect_requested.connect(self._effects.start_effect_handler)
        self._effects_qml_presentations_model.stop_effect_requested.connect(self._effects.stop_effect_handler)
        self._fader_page.change_effect_speed.connect(self._effects.set_effect_speed_handler)
        self._fader_page.change_effect_fade.connect(self._effects.set_effect_fade_handler)
        self._fader_page.change_dimmer_channel.connect(self._artnet_output.change_dimmer_channel_handler)
        self._fader_page.change_color_red_channel.connect(self._artnet_output.change_color_red_channel_handler)
        self._fader_page.change_color_green_channel.connect(self._artnet_output.change_color_green_channel_handler)
        self._fader_page.change_color_blue_channel.connect(self._artnet_output.change_color_blue_channel_handler)

        self._effects_qml_presentations_model.set_effect_cues_requested.connect(self._effects.set_effect_cues_handler)
        self._effects_qml_presentations_model.update_effect_cues_requested.connect(self._effects.get_effect_cues)
        self._effects.effect_cues_updated.connect(self._effects_qml_presentations_model.effect_cues_updated_handler)
        
        
        
    def setup(self) -> None:
        GPIO.setmode(GPIO.BCM)
        self._double_speed_rotary_encoder_0.setup()
        self._double_speed_rotary_encoder_1.setup()
        self._double_speed_rotary_encoder_2.setup()
        self._double_speed_rotary_encoder_3.setup()
        self._dmx_fixture_patch.setup()
        self._fixture_library.setup()
        self._dmx_list.setup()
        self._cue_list.setup()
        self._stage_view_qml_presentation_model.setup()

        self._artnet_manager.start_output()
        
        self.x_buttons.setup()
        self.k_keypad.setup()
        
        self._i2c_connection.start()
        
        self._fader_page.setup()
        
        

    def timer(self) -> None:
        self._gpio_based_rotary_encoder_driver_0.timer()
        self._gpio_based_rotary_encoder_driver_1.timer()
        self._gpio_based_rotary_encoder_driver_2.timer()
        self._gpio_based_rotary_encoder_driver_3.timer()
        
    def cleanup(self) -> None:
        GPIO.cleanup()

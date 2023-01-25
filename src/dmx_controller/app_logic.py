import RPi.GPIO as GPIO

from py_drivers.driver_rotary_encoder import GpioBasedRotaryEncoderDriver

from py_components.double_speed_rotary_encoder import DoubleSpeedRotaryEncoder
from py_components.rotary_encoder import RotaryEncoder

from py_qml_presentation_models.double_speed_rotary_encoder_qml_presentation_model import DoubleSpeedRotaryEncoderQmlPresentationModel
from py_qml_presentation_models.rotary_encoder_qml_presentation_model import RotaryEncoderQmlPresentationModel

from py_qml_presentation_models.qml_presentation_model_fixture import FixtureQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_dmx_fixture_patch import DmxFixturePatchQmlPresentationModel
from py_components.dmx_fixture_patch import DmxFixturePatch
from py_managers.fixture_manager import FixtureManager

from py_qml_presentation_models.qml_presentation_model_fixture_library import FixtureLibraryQmlPresentationModel
from py_components.fixture_library import FixtureLibrary

from py_qml_presentation_models.qml_presentation_model_color_picker import ColorPickerQmlPresentationModel
from py_components.color_picker import ColorPicker

from py_qml_presentation_models.qml_presentation_model_dmx_list import DmxListQmlPresentationModel
from py_components.dmx_list import DmxList


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
    GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_1: int = 13

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
    _dmx_fixture_patch: DmxFixturePatch
    _fixture_manager: FixtureManager
    
    _fixture_library_qml_presentation_model: FixtureLibraryQmlPresentationModel
    _fixture_library: FixtureLibrary
    
    _rgb_color_picker_qml_presentation_model: ColorPickerQmlPresentationModel # the QML presentation model representing the RGB color picker instance
    _rgb_color_picker: ColorPicker # the RGB color picker instance

    _dmx_list_qml_presentations_model: DmxListQmlPresentationModel
    
    def __init__(self, double_speed_rotary_encoder_qml_presentation_model_0: DoubleSpeedRotaryEncoderQmlPresentationModel,
                 double_speed_rotary_encoder_qml_presentation_model_1: DoubleSpeedRotaryEncoderQmlPresentationModel,
                 double_speed_rotary_encoder_qml_presentation_model_2: DoubleSpeedRotaryEncoderQmlPresentationModel,
                 double_speed_rotary_encoder_qml_presentation_model_3: DoubleSpeedRotaryEncoderQmlPresentationModel,
                 fixture_qml_presentation_models: list[FixtureQmlPresentationModel],
                 fixtures_qml_presentation_model: DmxFixturePatchQmlPresentationModel,
                 fixture_library_qml_presentation_model: FixtureLibraryQmlPresentationModel,
                 color_picker_qml_presentation_model: ColorPickerQmlPresentationModel,
                 dmx_list_qml_presentations_model: DmxListQmlPresentationModel,
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

        self._fixture_qml_presentation_models = fixture_qml_presentation_models
        self._fixtures_qml_presentation_model = fixtures_qml_presentation_model
        self._fixture_manager = FixtureManager()
        self._dmx_fixture_patch = DmxFixturePatch(self._fixture_manager)
        self._dmx_fixture_patch.fixtures_changed.connect(self._fixtures_qml_presentation_model.fixtures_changed)
        self._fixtures_qml_presentation_model.change_fixture_selected_status.connect(self._dmx_fixture_patch.change_fixture_selected_status_handler)        
        self._fixtures_qml_presentation_model.add_fixture_requested.connect(self._dmx_fixture_patch.add_fixture_handler)
        self._fixtures_qml_presentation_model.remove_fixture_requested.connect(self._dmx_fixture_patch.remove_fixture_handler)
        
        self._fixture_library_qml_presentation_model = fixture_library_qml_presentation_model
        self._fixture_library = FixtureLibrary(self._fixture_manager)
        self._fixture_library.library_fixtures_changed.connect(self._fixture_library_qml_presentation_model.library_fixtures_changed)
        
        # RGB color picker
        self._color_picker_qml_presentation_model = color_picker_qml_presentation_model
        self._rgb_color_picker = ColorPicker(self._double_speed_rotary_encoder_0,
                                                self._double_speed_rotary_encoder_1,
                                                self._double_speed_rotary_encoder_2)
        # connect signals of RGB color picker instance with slots of belonging QML presentation model (in both directions!)
        self._rgb_color_picker.r_changed.connect(self._color_picker_qml_presentation_model.r_changed)
        self._rgb_color_picker.g_changed.connect(self._color_picker_qml_presentation_model.g_changed)
        self._rgb_color_picker.b_changed.connect(self._color_picker_qml_presentation_model.b_changed)
        self._color_picker_qml_presentation_model.mixed_color_updated.connect(self._rgb_color_picker.change_mixed_color)
        
        self._dmx_list_qml_presentations_model = dmx_list_qml_presentations_model
        self._fixture_manager = FixtureManager()
        self._dmx_list: DmxList = DmxList(self._fixture_manager)
        self._dmx_list.dmx_data_changed.connect(self._dmx_list_qml_presentations_model.list_updated)
     
        
    def setup(self) -> None:
        GPIO.setmode(GPIO.BCM)
        self._double_speed_rotary_encoder_0.setup()
        self._double_speed_rotary_encoder_1.setup()
        self._double_speed_rotary_encoder_2.setup()
        self._double_speed_rotary_encoder_3.setup()
        self._dmx_fixture_patch.setup()
        self._fixture_library.setup()
        self._dmx_list.setup()

    def timer(self) -> None:
        self._gpio_based_rotary_encoder_driver_0.timer()
        self._gpio_based_rotary_encoder_driver_1.timer()
        self._gpio_based_rotary_encoder_driver_2.timer()
        self._gpio_based_rotary_encoder_driver_3.timer()

    def cleanup(self) -> None:
        self._gpio_based_rotary_encoder_driver_3.cleanup()
        self._gpio_based_rotary_encoder_driver_2.cleanup()
        self._gpio_based_rotary_encoder_driver_1.cleanup()
        self._gpio_based_rotary_encoder_driver_0.cleanup()
        GPIO.cleanup()

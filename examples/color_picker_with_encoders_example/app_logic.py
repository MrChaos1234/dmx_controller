import RPi.GPIO as GPIO

from rotary_encoder import RotaryEncoder

from main_presentation_model import MainPresentationModel
from rotary_encoder_presentation_model import RotaryEncoderPresentationModel


class AppLogic(object):
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

    STATE_ON: int = 1
    STATE_OFF: int = 0

    # presentation model for the general content of the main window
    main_presentation_model: MainPresentationModel
    # presentation models for the rotary encoder 0..3 displayed on the main window
    rotary_encoder_presentation_models: list[RotaryEncoderPresentationModel]
    # external timer frequency for debouncing the push button signals
    debouncing_external_timer_frequency: int
    # instances to controll the hardware of the rotary encoders 0..3
    rotary_encoders: list[RotaryEncoder]
    # positions of the rotary encoders 0..3
    rotary_encoder_positions: list[int]
    # min boundaries for the positions of the rotary encoders 0..3
    rotary_encoder_mins: list[int]
    # max boundaries for the positions of the rotary encoders 0..3
    rotary_encoder_maxs: list[int]
    # state on/off of the rotary encoders 0..3 / pressing the pushbutton toggles the state between STATE_ON=1 and STATE_OFF=0
    rotary_encoder_states: list[int]

    def __init__(self, main_presentation_model: MainPresentationModel,
                 rotary_encoder_presentation_models: list[RotaryEncoderPresentationModel],
                 debouncing_external_timer_frequency: int):
        self.main_presentation_model = main_presentation_model
        self.rotary_encoder_presentation_models = rotary_encoder_presentation_models
        self.debouncing_external_timer_frequency = debouncing_external_timer_frequency
        self.rotary_encoders = []
        self.rotary_encoder_positions = []
        self.rotary_encoder_mins = []
        self.rotary_encoder_maxs = []
        self.rotary_encoder_states = []
        # self.rotary_encoder_purposes = []

        self._create_rotary_encoder(0,
                                    self.GPIO_NUMBER_ROTARY_ENCODER_A_0, self.GPIO_NUMBER_ROTARY_ENCODER_B_0, self.GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_0,
                                    0, 0, 255)
        self._create_rotary_encoder(1,
                                    self.GPIO_NUMBER_ROTARY_ENCODER_A_1, self.GPIO_NUMBER_ROTARY_ENCODER_B_1, self.GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_1,
                                    0, 0, 255)
        self._create_rotary_encoder(2,
                                    self.GPIO_NUMBER_ROTARY_ENCODER_A_2, self.GPIO_NUMBER_ROTARY_ENCODER_B_2, self.GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_2,
                                    0, 0, 255)
        self._create_rotary_encoder(3,
                                    self.GPIO_NUMBER_ROTARY_ENCODER_A_3, self.GPIO_NUMBER_ROTARY_ENCODER_B_3, self.GPIO_NUMBER_ROTARY_ENCODER_PUSHBUTTON_3,
                                    0, 0, 255)

    def _create_rotary_encoder(self, rotary_encoder_index: int, gpio_number_a: int, gpio_number_b: int, gpio_number_pushbutton: int, position: int, min: int, max: int) -> None:
        self.rotary_encoders.append(RotaryEncoder(gpio_number_a, gpio_number_b, gpio_number_pushbutton,
                                    self._rotary_encoder_rotated_clockwise_callback, self._rotary_encoder_rotated_counterclockwise_callback,
                                    self._rotary_encoder_pushbutton_pressed_callback, self._rotary_encoder_pushbutton_released_callback,
                                    rotary_encoder_index, self.debouncing_external_timer_frequency))
        self.rotary_encoder_positions.append(position)
        self.rotary_encoder_mins.append(min)
        self.rotary_encoder_maxs.append(max)
        self.rotary_encoder_states.append(self.STATE_OFF)
        # self.rotary_encoder_purposes.append(purpose)

    def _rotary_encoder_rotated_clockwise_callback(self, instance_data: object) -> None:
        rotary_encoder_index: int = instance_data
        # if button is pressed while rotating, move in steps of 10
        if self.rotary_encoder_states[rotary_encoder_index] == self.STATE_ON:
            self.rotary_encoder_positions[rotary_encoder_index] += 10
        else:
            self.rotary_encoder_positions[rotary_encoder_index] += 1

        self._check_and_limit_rotary_encoder_position(rotary_encoder_index)
        self.rotary_encoder_presentation_models[
            rotary_encoder_index].position = self.rotary_encoder_positions[rotary_encoder_index]

    def _check_and_limit_rotary_encoder_position(self, rotary_encoder_index: int) -> None:
        if self.rotary_encoder_positions[rotary_encoder_index] > self.rotary_encoder_maxs[rotary_encoder_index]:
            self.rotary_encoder_positions[rotary_encoder_index] = self.rotary_encoder_maxs[rotary_encoder_index]
        if self.rotary_encoder_positions[rotary_encoder_index] < self.rotary_encoder_mins[rotary_encoder_index]:
            self.rotary_encoder_positions[rotary_encoder_index] = self.rotary_encoder_mins[rotary_encoder_index]

    def _rotary_encoder_rotated_counterclockwise_callback(self, instance_data: object) -> None:
        rotary_encoder_index: int = instance_data
        # if button is pressed while rotating, move in steps of 10
        if self.rotary_encoder_states[rotary_encoder_index] == self.STATE_ON:
            self.rotary_encoder_positions[rotary_encoder_index] -= 10
        else:
            self.rotary_encoder_positions[rotary_encoder_index] -= 1

        self._check_and_limit_rotary_encoder_position(rotary_encoder_index)
        self.rotary_encoder_presentation_models[
            rotary_encoder_index].position = self.rotary_encoder_positions[rotary_encoder_index]

    def _rotary_encoder_pushbutton_pressed_callback(self, instance_data: object) -> None:

        rotary_encoder_index: int = instance_data
        self.rotary_encoder_presentation_models[rotary_encoder_index].press_pushbutton(
        )

    def _rotary_encoder_pushbutton_released_callback(self, instance_data: object) -> None:
        rotary_encoder_index: int = instance_data
        self.rotary_encoder_presentation_models[rotary_encoder_index].release_pushbutton(
        )
        self._toggle_rotary_encoder_state(rotary_encoder_index)
        self.rotary_encoder_presentation_models[
            rotary_encoder_index].state = self.rotary_encoder_states[rotary_encoder_index]

    def _toggle_rotary_encoder_state(self, rotary_encoder_index: int) -> None:
        if self.rotary_encoder_states[rotary_encoder_index] == self.STATE_OFF:
            self.rotary_encoder_states[rotary_encoder_index] = self.STATE_ON
        else:
            self.rotary_encoder_states[rotary_encoder_index] = self.STATE_OFF

    def setup(self) -> None:
        rotary_encoder_index: int
        for rotary_encoder_index in range(4):
            self._rotary_encoder_presentation_model_setup(rotary_encoder_index)

        GPIO.setmode(GPIO.BCM)

        for rotary_encoder_index in range(4):
            self.rotary_encoders[rotary_encoder_index].setup()

    def _rotary_encoder_presentation_model_setup(self, rotary_encoder_index: int) -> None:
        self.rotary_encoder_presentation_models[
            rotary_encoder_index].position = self.rotary_encoder_positions[rotary_encoder_index]
        self.rotary_encoder_presentation_models[rotary_encoder_index].min = self.rotary_encoder_mins[rotary_encoder_index]
        self.rotary_encoder_presentation_models[rotary_encoder_index].max = self.rotary_encoder_maxs[rotary_encoder_index]

    def timer(self) -> None:
        rotary_encoder_index: int
        for rotary_encoder_index in range(4):
            self.rotary_encoders[rotary_encoder_index].timer()

    def cleanup(self) -> None:
        rotary_encoder_index: int
        for rotary_encoder_index in range(4):
            self.rotary_encoders[rotary_encoder_index].cleanup()

        GPIO.cleanup()

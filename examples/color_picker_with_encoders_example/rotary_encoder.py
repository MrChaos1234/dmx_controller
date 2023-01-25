from typing import Callable

from enum import Enum, auto
import RPi.GPIO as GPIO


class RotaryEncoder(object):
    PUSHBUTTON_EXTERNAL_TIMER_FRQUENCY_DEFAULT: int = 100 # 100 Hz for external timer frequency as default for debouncing the push button of the rotary encoder
    PUSHBUTTON_DEBOUNCE_TIME_DEFAULT: int = 30 # 30 ms debounce time as default for push button of rotary encoder

    class EncoderState(Enum): # possible states for internal state machine
        UNKNOWN = auto()
        B_FALLED_FIRST = auto()
        A_FALLED_SECOND = auto()
        B_RISED_FIRST = auto()
        A_RISED_SECOND = auto()
        A_FALLED_FIRST = auto()
        B_FALLED_SECOND = auto()
        A_RISED_FIRST = auto()
        B_RISED_SECOND = auto()

    class PushbuttonState(Enum): # possible states for the debounced push button signal
        RELEASED = auto()
        PRESSED = auto()

    encoder_state: EncoderState # state of internal state machine
    pushbutton_state: PushbuttonState # state of debounced push button signal
    pushbutton_integrator: int # integrated signal for debouncing the push button signal (see http://www.kennethkuhn.com/electronics/debounce.c for details)
    pushbutton_integrator_max: int # max value possible for integrated signal for debouncing the push button signal
    gpio_number_signal_a: int # number of GPIO (not pin number!) for signal A
    gpio_number_signal_b: int # number of GPIO (not pin number!) for signal B
    gpio_number_signal_pushbutton: int # number of GPIO (not pin number!) for signal of pushbutton
    rotated_clockwise_callback: Callable # callback called, if encoder is rotated clockwise
    rotated_counterclockwise_callback: Callable # callback called, if encoder is rotated counterclockwise
    pushbutton_pressed_callback: Callable # callback called, if pushbutton is pressed
    pushbutton_released_callback: Callable # callback called, if pushbutton is released
    instance_data: object # user defined data belonging to this instance of the RotaryEncoder class
    pushbutton_external_timer_frequency: int # external timer frequency for debouncing the push button signal
    pushbutton_debounce_time: int # deounce time for push button signal

    def __init__(self, gpio_number_signal_a: int, 
                       gpio_number_signal_b: int, 
                       gpio_number_signal_pushbutton: int, 
                       rotated_clockwise_callback: Callable,
                       rotated_counterclockwise_callback: Callable,
                       pushbutton_pressed_callback: Callable,
                       pushbutton_released_callback: Callable,
                       instance_data: object = None,
                       pushbutton_external_timer_frequency: int = PUSHBUTTON_EXTERNAL_TIMER_FRQUENCY_DEFAULT,
                       pushbutton_debounce_time: int = PUSHBUTTON_DEBOUNCE_TIME_DEFAULT):
        self.encoder_state = self.EncoderState.UNKNOWN
        self.pushbutton_state = self.PushbuttonState.RELEASED
        self.pushbutton_integrator = 0
        self.pushbutton_integrator_max = (pushbutton_debounce_time / 1000) / pushbutton_external_timer_frequency
        self.gpio_number_signal_a = gpio_number_signal_a
        self.gpio_number_signal_b = gpio_number_signal_b
        self.gpio_number_signal_pushbutton = gpio_number_signal_pushbutton
        self.rotated_clockwise_callback = rotated_clockwise_callback
        self.rotated_counterclockwise_callback = rotated_counterclockwise_callback
        self.pushbutton_pressed_callback = pushbutton_pressed_callback
        self.pushbutton_released_callback = pushbutton_released_callback
        self.instance_data = instance_data
        self.pushbutton_external_timer_frequency = pushbutton_external_timer_frequency
        self.pushbutton_debounce_time = pushbutton_debounce_time

    def _a_changed_callback(self, channel: int) -> None:
        if channel == self.gpio_number_signal_a:
            # A changed
            if GPIO.input(self.gpio_number_signal_a):
                # A rised
                if self.encoder_state == self.EncoderState.B_RISED_FIRST:
                    self.encoder_state = self.EncoderState.A_RISED_SECOND
                    self.rotated_clockwise_callback(self.instance_data)
                    self.encoder_state = self.EncoderState.UNKNOWN
                elif self.encoder_state == self.EncoderState.B_FALLED_SECOND:
                    self.encoder_state = self.EncoderState.A_RISED_FIRST
            else:
                # A falled
                if self.encoder_state == self.EncoderState.B_FALLED_FIRST:
                    self.encoder_state = self.EncoderState.A_FALLED_SECOND
                elif self.encoder_state == self.EncoderState.UNKNOWN:
                    self.encoder_state = self.EncoderState.A_FALLED_FIRST

    def _b_changed_callback(self, channel: int) -> None:
        if channel == self.gpio_number_signal_b:
            # B changed
            if GPIO.input(self.gpio_number_signal_b):
                # B rised
                if self.encoder_state == self.EncoderState.A_FALLED_SECOND:
                    self.encoder_state = self.EncoderState.B_RISED_FIRST
                elif self.encoder_state == self.EncoderState.A_RISED_FIRST:
                    self.encoder_state = self.EncoderState.B_RISED_SECOND
                    self.rotated_counterclockwise_callback(self.instance_data)
                    self.encoder_state = self.EncoderState.UNKNOWN
            else:
                # B falled
                if self.encoder_state == self.EncoderState.UNKNOWN:
                    self.encoder_state = self.EncoderState.B_FALLED_FIRST
                elif self.encoder_state == self.EncoderState.A_FALLED_FIRST:
                    self.encoder_state = self.EncoderState.B_FALLED_SECOND

    def setup(self) -> None:
        GPIO.setup(self.gpio_number_signal_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.gpio_number_signal_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.gpio_number_signal_pushbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.gpio_number_signal_a, GPIO.BOTH, callback=self._a_changed_callback)
        GPIO.add_event_detect(self.gpio_number_signal_b, GPIO.BOTH, callback=self._b_changed_callback)

    def timer(self) -> None:
        pushbutton_signal: bool = not GPIO.input(self.gpio_number_signal_pushbutton) # push button signal is pulled up against VCC; 
                                                                                     # inverting it here to get True for pressed button
        # update the integrator for debouncing
        if not pushbutton_signal:
            if self.pushbutton_integrator > 0:
                self.pushbutton_integrator -= 1
        elif self.pushbutton_integrator < self.pushbutton_integrator_max:
            self.pushbutton_integrator += 1
        # update debounced output signal
        if self.pushbutton_integrator <= 0:
            if self.pushbutton_state == self.PushbuttonState.PRESSED:
                self.pushbutton_state = self.PushbuttonState.RELEASED
                self.pushbutton_released_callback(self.instance_data)
        elif self.pushbutton_integrator >= self.pushbutton_integrator_max:
            if self.pushbutton_state == self.PushbuttonState.RELEASED:
                self.pushbutton_state = self.PushbuttonState.PRESSED
                self.pushbutton_pressed_callback(self.instance_data)

    def cleanup(self) -> None:
        GPIO.remove_event_detect(self.gpio_number_signal_b)
        GPIO.remove_event_detect(self.gpio_number_signal_a)

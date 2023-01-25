from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from enum import Enum, auto
import RPi.GPIO as GPIO


class GpioBasedRotaryEncoderDriver(QObject):
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

    rotated_clockwise: pyqtSignal = pyqtSignal(object)
    rotated_counterclockwise: pyqtSignal = pyqtSignal(object)
    pushbutton_pressed: pyqtSignal = pyqtSignal(object)
    pushbutton_released: pyqtSignal = pyqtSignal(object)

    _encoder_state: EncoderState # state of internal state machine
    _pushbutton_state: PushbuttonState # state of debounced push button signal
    _pushbutton_integrator: int # integrated signal for debouncing the push button signal (see http://www.kennethkuhn.com/electronics/debounce.c for details)
    _pushbutton_integrator_max: int # max value possible for integrated signal for debouncing the push button signal
    _gpio_number_signal_a: int # number of GPIO (not pin number!) for signal A
    _gpio_number_signal_b: int # number of GPIO (not pin number!) for signal B
    _gpio_number_signal_pushbutton: int # number of GPIO (not pin number!) for signal of pushbutton
    _pushbutton_external_timer_frequency: int # external timer frequency for debouncing the push button signal
    _pushbutton_debounce_time: int # deounce time for push button signal
    _instance_data: object # user defined data belonging to this instance of the GpioBasedRotaryEncoderDriver class

    def __init__(self, gpio_number_signal_a: int, 
                       gpio_number_signal_b: int, 
                       gpio_number_signal_pushbutton: int, 
                       pushbutton_external_timer_frequency: int = PUSHBUTTON_EXTERNAL_TIMER_FRQUENCY_DEFAULT,
                       pushbutton_debounce_time: int = PUSHBUTTON_DEBOUNCE_TIME_DEFAULT,
                       instance_data: object = None,
                       parent: QObject = None):
        super().__init__(parent)
        self._encoder_state = self.EncoderState.UNKNOWN
        self._pushbutton_state = self.PushbuttonState.RELEASED
        self._pushbutton_integrator = 0
        self._pushbutton_integrator_max = (pushbutton_debounce_time / 1000) / pushbutton_external_timer_frequency
        self._gpio_number_signal_a = gpio_number_signal_a
        self._gpio_number_signal_b = gpio_number_signal_b
        self._gpio_number_signal_pushbutton = gpio_number_signal_pushbutton
        self._instance_data = instance_data
        self._pushbutton_external_timer_frequency = pushbutton_external_timer_frequency
        self._pushbutton_debounce_time = pushbutton_debounce_time

    def _a_changed_callback(self, channel: int) -> None:
        if channel == self._gpio_number_signal_a:
            # A changed
            if GPIO.input(self._gpio_number_signal_a):
                # A rised
                if self._encoder_state == self.EncoderState.B_RISED_FIRST:
                    self._encoder_state = self.EncoderState.A_RISED_SECOND
                    self.rotated_clockwise.emit(self._instance_data)
                    self._encoder_state = self.EncoderState.UNKNOWN
                elif self._encoder_state == self.EncoderState.B_FALLED_SECOND:
                    self._encoder_state = self.EncoderState.A_RISED_FIRST
            else:
                # A falled
                if self._encoder_state == self.EncoderState.B_FALLED_FIRST:
                    self._encoder_state = self.EncoderState.A_FALLED_SECOND
                elif self._encoder_state == self.EncoderState.UNKNOWN:
                    self._encoder_state = self.EncoderState.A_FALLED_FIRST

    def _b_changed_callback(self, channel: int) -> None:
        if channel == self._gpio_number_signal_b:
            # B changed
            if GPIO.input(self._gpio_number_signal_b):
                # B rised
                if self._encoder_state == self.EncoderState.A_FALLED_SECOND:
                    self._encoder_state = self.EncoderState.B_RISED_FIRST
                elif self._encoder_state == self.EncoderState.A_RISED_FIRST:
                    self._encoder_state = self.EncoderState.B_RISED_SECOND
                    self.rotated_counterclockwise.emit(self._instance_data)
                    self._encoder_state = self.EncoderState.UNKNOWN
            else:
                # B falled
                if self._encoder_state == self.EncoderState.UNKNOWN:
                    self._encoder_state = self.EncoderState.B_FALLED_FIRST
                elif self._encoder_state == self.EncoderState.A_FALLED_FIRST:
                    self._encoder_state = self.EncoderState.B_FALLED_SECOND

    def setup(self) -> None:
        GPIO.setup(self._gpio_number_signal_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._gpio_number_signal_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._gpio_number_signal_pushbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self._gpio_number_signal_a, GPIO.BOTH, callback=self._a_changed_callback)
        GPIO.add_event_detect(self._gpio_number_signal_b, GPIO.BOTH, callback=self._b_changed_callback)

    @pyqtSlot()
    def timer(self) -> None:
        pushbutton_signal: bool = not GPIO.input(self._gpio_number_signal_pushbutton) # push button signal is pulled up against VCC; 
                                                                                      # inverting it here to get True for pressed button
        # update the integrator for debouncing
        if not pushbutton_signal:
            if self._pushbutton_integrator > 0:
                self._pushbutton_integrator -= 1
        elif self._pushbutton_integrator < self._pushbutton_integrator_max:
            self._pushbutton_integrator += 1
        # update debounced output signal
        if self._pushbutton_integrator <= 0:
            if self._pushbutton_state == self.PushbuttonState.PRESSED:
                self._pushbutton_state = self.PushbuttonState.RELEASED
                self.pushbutton_released.emit(self._instance_data)
        elif self._pushbutton_integrator >= self._pushbutton_integrator_max:
            if self._pushbutton_state == self.PushbuttonState.RELEASED:
                self._pushbutton_state = self.PushbuttonState.PRESSED
                self.pushbutton_pressed.emit(self._instance_data)

    def cleanup(self) -> None:
        GPIO.remove_event_detect(self._gpio_number_signal_b)
        GPIO.remove_event_detect(self._gpio_number_signal_a)

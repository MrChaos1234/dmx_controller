from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from py_components.double_speed_rotary_encoder import DoubleSpeedRotaryEncoder


class ColorPicker(QObject):
    r_changed: pyqtSignal = pyqtSignal(int)
    g_changed: pyqtSignal = pyqtSignal(int)
    b_changed: pyqtSignal = pyqtSignal(int)
    dimmer_changed: pyqtSignal = pyqtSignal(int)
    
    _double_speed_rotary_encoder_r: DoubleSpeedRotaryEncoder # the instance of the DoubleSpeedRotaryEncoder class representing the R part of the color
    _double_speed_rotary_encoder_g: DoubleSpeedRotaryEncoder # the instance of the DoubleSpeedRotaryEncoder class representing the G part of the color
    _double_speed_rotary_encoder_b: DoubleSpeedRotaryEncoder # the instance of the DoubleSpeedRotaryEncoder class representing the B part of the color
    _double_speed_rotary_encoder_dimmer: DoubleSpeedRotaryEncoder # the instance of the DoubleSpeedRotaryEncoder class representing the dimmer
    _r: int # R part of the color
    _g: int # G part of the color
    _b: int # B part of the color
    _dimmer: int
    _instance_data_r: object # user defined data belonging to the instance of the DoubleSpeedRotaryEncoder class representing the R part of the color
    _instance_data_g: object # user defined data belonging to the instance of the DoubleSpeedRotaryEncoder class representing the G part of the color
    _instance_data_b: object # user defined data belonging to the instance of the DoubleSpeedRotaryEncoder class representing the B part of the color
    _instance_data_dimmer: object # user defined data belonging to the instance of the DoubleSpeedRotaryEncoder class representing the dimmer

    def __init__(self,
                 double_speed_rotary_encoder_r: DoubleSpeedRotaryEncoder,
                 double_speed_rotary_encoder_g: DoubleSpeedRotaryEncoder,
                 double_speed_rotary_encoder_b: DoubleSpeedRotaryEncoder,
                 double_speed_rotary_encoder_dimmer: DoubleSpeedRotaryEncoder,
                 instance_data_r: object = None,
                 instance_data_g: object = None,
                 instance_data_b: object = None,
                 instance_data_dimmer: object = None,
                 parent: QObject = None):
        super().__init__(parent)
        self._double_speed_rotary_encoder_r = double_speed_rotary_encoder_r
        self._double_speed_rotary_encoder_g = double_speed_rotary_encoder_g
        self._double_speed_rotary_encoder_b = double_speed_rotary_encoder_b
        self._double_speed_rotary_encoder_dimmer = double_speed_rotary_encoder_dimmer
        self._instance_data_r = instance_data_r
        self._instance_data_g = instance_data_g
        self._instance_data_b = instance_data_b
        self._instance_data_dimmer = instance_data_dimmer
        self._r = 0
        self._g = 0
        self._b = 0
        self._dimmer = 0
        # connect positions of deouble speed rotary encoder hardware instances with slots
        self._double_speed_rotary_encoder_r.position_changed.connect(self._r_position_changed)
        self._double_speed_rotary_encoder_g.position_changed.connect(self._g_position_changed)
        self._double_speed_rotary_encoder_b.position_changed.connect(self._b_position_changed)
        self._double_speed_rotary_encoder_dimmer.position_changed.connect(self._dimmer_position_changed)

    @pyqtSlot(object, int)
    def _r_position_changed(self, instance_data: object, position: int) -> None:
        if instance_data == self._instance_data_r:
            self._r = position
            self.r_changed.emit(self._r)

    @pyqtSlot(object, int)
    def _g_position_changed(self, instance_data: object, position: int) -> None:
        if instance_data == self._instance_data_g:
            self._g = position
            self.g_changed.emit(self._g)

    @pyqtSlot(object, int)
    def _b_position_changed(self, instance_data: object, position: int) -> None:
        if instance_data == self._instance_data_b:
            self._b = position
            self.b_changed.emit(self._b)
    
    @pyqtSlot(object, int)
    def _dimmer_position_changed(self, instance_data: object, position: int) -> None:
        if instance_data == self._instance_data_dimmer:
            self._dimmer = position
            self.dimmer_changed.emit(self._dimmer)

    @pyqtSlot(int, int, int)
    def change_mixed_color(self, r: int, g: int, b: int) -> None:
        """Changes the R, G and B parts of the color, but does not emit the belonging Qt signals r_changed, g_changed and b_changed"""
        self._r = r
        self._g = g
        self._b = b
        self._double_speed_rotary_encoder_r.set_position(self._r)
        self._double_speed_rotary_encoder_g.set_position(self._g)
        self._double_speed_rotary_encoder_b.set_position(self._b)

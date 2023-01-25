#!/usr/bin/env python3

import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QTimer

from threads.i2c_thread import I2cThread
from py_components.k_keypad import KKeypad
from py_components.hardware_led import HardwareLed


from py_qml_presentation_models.qml_presentation_model_k_keypad import KKeypadQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_hardware_led import HardwareLedQmlPresentationModel
from py_qml_presentation_models.double_speed_rotary_encoder_qml_presentation_model import DoubleSpeedRotaryEncoderQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_dmx_fixture_patch import DmxFixturePatchQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_fixture import FixtureQmlPresentationModel, LibraryFixtureQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_dmx_fixture_patch import DmxFixturePatchQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_fixture_library import FixtureLibraryQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_color_picker import ColorPickerQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_dmx_list import DmxListQmlPresentationModel
from py_qml_presentation_models.qml_presentation_model_dmx_channel import DmxChannelQmlPresentationModel

from app_logic import AppLogic


def main():
    # 100 Hz for external timer frequency as default for debouncing the push button signals of the rotary encoders
    DEBOUNCING_EXTERNAL_TIMER_FRQUENCY: int = 100

    app: QGuiApplication = QGuiApplication(sys.argv)
    engine: QQmlApplicationEngine = QQmlApplicationEngine()

    # # Create an Object of the I2cThread class
    # i2c_connection: I2cThread = I2cThread()
    # # Create an Object of the KKeypad class
    # k_keypad: KKeypad = KKeypad(i2c_connection)
    # # Create an Object of the HardwareLed class
    # hardware_leds: HardwareLed = HardwareLed(i2c_connection)

    # # Create an Object of the KKeypadQmlPresentationModel class
    # k_keypad_qml_presentation_model: KKeypadQmlPresentationModel = KKeypadQmlPresentationModel()
    # # Create an Object of the HardwareLedQmlPresentationModel class
    # hardware_leds_qml_presentation_model: HardwareLedQmlPresentationModel = HardwareLedQmlPresentationModel()

    double_speed_rotary_encoder_qml_presentation_model_0: DoubleSpeedRotaryEncoderQmlPresentationModel = DoubleSpeedRotaryEncoderQmlPresentationModel()
    double_speed_rotary_encoder_qml_presentation_model_1: DoubleSpeedRotaryEncoderQmlPresentationModel = DoubleSpeedRotaryEncoderQmlPresentationModel()
    double_speed_rotary_encoder_qml_presentation_model_2: DoubleSpeedRotaryEncoderQmlPresentationModel = DoubleSpeedRotaryEncoderQmlPresentationModel()
    double_speed_rotary_encoder_qml_presentation_model_3: DoubleSpeedRotaryEncoderQmlPresentationModel = DoubleSpeedRotaryEncoderQmlPresentationModel()

    fixture_qml_presentation_models: list[FixtureQmlPresentationModel] = []
    fixtures_qml_presentation_model: DmxFixturePatchQmlPresentationModel = DmxFixturePatchQmlPresentationModel(fixture_qml_presentation_models, engine)

    library_fixture_qml_presentation_models: list[LibraryFixtureQmlPresentationModel] = []
    fixture_library_qml_presentation_model: FixtureLibraryQmlPresentationModel = FixtureLibraryQmlPresentationModel(library_fixture_qml_presentation_models, engine)
    
    color_picker_qml_presentation_model: ColorPickerQmlPresentationModel = ColorPickerQmlPresentationModel(None, engine)
   
    dmx_list_qml_presentations_models: list[DmxChannelQmlPresentationModel] = []
    dmx_list_qml_presentations_model: DmxListQmlPresentationModel = DmxListQmlPresentationModel(dmx_list_qml_presentations_models, engine)
    
    app_logic: AppLogic = AppLogic(double_speed_rotary_encoder_qml_presentation_model_0,
                                   double_speed_rotary_encoder_qml_presentation_model_1,
                                   double_speed_rotary_encoder_qml_presentation_model_2,
                                   double_speed_rotary_encoder_qml_presentation_model_3,
                                   fixture_qml_presentation_models,
                                   fixtures_qml_presentation_model,
                                   fixture_library_qml_presentation_model,
                                   color_picker_qml_presentation_model,
                                   dmx_list_qml_presentations_model,
                                   DEBOUNCING_EXTERNAL_TIMER_FRQUENCY)

    ##### NO KEYPAD OR LEDS #####
    # # Connect the key_pressed signal of the KKeypad class to the key_pressed_handler slot of the KKeypadQmlPresentationModel class
    # k_keypad.key_pressed.connect(
    #     k_keypad_qml_presentation_model.key_pressed_handler)
    # # Connect the key_released signal of the KKeypad class to the key_released_handler slot of the KKeypadQmlPresentationModel class
    # k_keypad.key_released.connect(
    #     k_keypad_qml_presentation_model.key_released_handler)

    # # Connect the hardware_led_color_change signal of the HardwareLedQmlPresentationModel class to the change_led_color slot of the Led class
    # hardware_leds_qml_presentation_model.hardware_led_color_change.connect(
    #     hardware_leds.change_led_color)
    # # Connect the led_color_change signal of the Led class to the led_color_change_handler slot of the I2cThread class
    # hardware_leds.hardware_led_color_change.connect(
    #     i2c_connection.led_color_change_handler)


    engine.quit.connect(app.quit)
    # engine.rootContext().setContextProperty('kKeypadQmlPresentationModel',
    #                                         k_keypad_qml_presentation_model)  # Make the KKeypadQmlPresentationModel class available to QML
    # engine.rootContext().setContextProperty('hardwareLedQmlPresentationModel',
    #                                         hardware_leds_qml_presentation_model)  # Make the KKeypadQmlPresentationModel class available to QML
    engine.rootContext().setContextProperty('doubleSpeedRotaryEncoderQmlPresentationModel0',
                                            double_speed_rotary_encoder_qml_presentation_model_0)
    engine.rootContext().setContextProperty('doubleSpeedRotaryEncoderQmlPresentationModel1',
                                            double_speed_rotary_encoder_qml_presentation_model_1)
    engine.rootContext().setContextProperty('doubleSpeedRotaryEncoderQmlPresentationModel2',
                                            double_speed_rotary_encoder_qml_presentation_model_2)
    engine.rootContext().setContextProperty('doubleSpeedRotaryEncoderQmlPresentationModel3',
                                            double_speed_rotary_encoder_qml_presentation_model_3)

    # Make the Led class available to QML
    # engine.rootContext().setContextProperty('hardwareLeds', hardware_leds)
    
    engine.rootContext().setContextProperty('dmxFixturePatchQmlPresentationModel', fixtures_qml_presentation_model)
    engine.rootContext().setContextProperty('fixtureLibraryQmlPresentationModel', fixture_library_qml_presentation_model)
    engine.rootContext().setContextProperty('colorPickerQmlPresentationModel', color_picker_qml_presentation_model)
    engine.rootContext().setContextProperty('dmxListQmlPresentationModel', dmx_list_qml_presentations_model)
    engine.load('MainWindow.qml')

    # Setup for Aplogic -> rotary encoders
    app_logic.setup()
    timer: QTimer = QTimer()
    timer.setInterval(int(1000 / DEBOUNCING_EXTERNAL_TIMER_FRQUENCY))
    timer.timeout.connect(app_logic.timer)
    timer.start()

    # i2c_connection.start()  # Start the I2cThread
    # Further Threads can be started here

    app_exit_code: int = app.exec()

    #i2c_connection.stop_and_wait()  # Stop the I2cThread
    # Further Threads can be stopped here

    sys.exit(app_exit_code)


if __name__ == "__main__":
    main()

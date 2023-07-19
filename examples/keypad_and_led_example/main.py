#!/usr/bin/env python3

import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from i2c_thread import I2cThread
from k_keypad import KKeypad
from x_buttons import XButtons
from hardware_led import HardwareLed

from qml_presentation_model_k_keypad import KKeypadQmlPresentationModel
from qml_presentation_model_hardware_led import HardwareLedQmlPresentationModel
from qml_presentation_model_x_buttons import XButtonsQmlPresentationModel

def main():

    i2c_connection: I2cThread = I2cThread()  # Create an Object of the I2cThread class
    k_keypad: KKeypad = KKeypad(i2c_connection)  # Create an Object of the KKeypad class
    hardware_leds: HardwareLed = HardwareLed(i2c_connection)  # Create an Object of the HardwareLed class
    x_buttons: XButtons = XButtons(i2c_connection)  # Create an Object of the XButtons class

    k_keypad_qml_presentation_model: KKeypadQmlPresentationModel = KKeypadQmlPresentationModel()  # Create an Object of the KKeypadQmlPresentationModel class
    hardware_leds_qml_presentation_model: HardwareLedQmlPresentationModel = HardwareLedQmlPresentationModel()  # Create an Object of the HardwareLedQmlPresentationModel class
    x_buttons_qml_presentation_model: XButtonsQmlPresentationModel = XButtonsQmlPresentationModel()  # Create an Object of the XButtonsQmlPresentationModel class
    
    k_keypad.key_pressed.connect(k_keypad_qml_presentation_model.key_pressed_handler)  # Connect the key_pressed signal of the KKeypad class to the key_pressed_handler slot of the KKeypadQmlPresentationModel class
    k_keypad.key_released.connect(k_keypad_qml_presentation_model.key_released_handler)  # Connect the key_released signal of the KKeypad class to the key_released_handler slot of the KKeypadQmlPresentationModel class
    
    x_buttons.x_key_pressed.connect(x_buttons_qml_presentation_model.x_key_pressed_handler)  # Connect the x_key_pressed signal of the XButtons class to the key_pressed_handler slot of the XButtonsQmlPresentationModel class
    x_buttons.x_key_released.connect(x_buttons_qml_presentation_model.x_key_released_handler)  # Connect the x_key_released signal of the XButtons class to the key_released_handler slot of the XButtonsQmlPresentationModel class
    
    hardware_leds_qml_presentation_model.hardware_led_color_change.connect(hardware_leds.change_led_color)  # Connect the hardware_led_color_change signal of the HardwareLedQmlPresentationModel class to the change_led_color slot of the Led class
    
    hardware_leds.hardware_led_color_change.connect(i2c_connection.led_color_change_handler) # Connect the led_color_change signal of the Led class to the led_color_change_handler slot of the I2cThread class
        
    app: QGuiApplication = QGuiApplication(sys.argv) 
    engine: QQmlApplicationEngine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.rootContext().setContextProperty('kKeypadQmlPresentationModel', k_keypad_qml_presentation_model)  # Make the KKeypadQmlPresentationModel class available to QML
    engine.rootContext().setContextProperty('hardwareLedQmlPresentationModel', hardware_leds_qml_presentation_model)  # Make the KKeypadQmlPresentationModel class available to QML
    engine.rootContext().setContextProperty('hardwareLeds', hardware_leds)  # Make the Led class available to QML
    engine.rootContext().setContextProperty('xButtonsQmlPresentationModel', x_buttons_qml_presentation_model)  # Make the XButtonsQmlPresentationModel class available to QML
    engine.load('MainWindow.qml')

    i2c_connection.start()  # Start the I2cThread
    # Further Threads can be started here

    app_exit_code: int = app.exec()

    i2c_connection.stop_and_wait() # Stop the I2cThread
    # Further Threads can be stopped here

    sys.exit(app_exit_code)


if __name__ == "__main__":
    main()

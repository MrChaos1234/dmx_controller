#!/usr/bin/env python3

import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from i2c_thread import I2cThread
from k_keypad import KKeypad

from qml_presentation_model_k_keypad import KKeypadQmlPresentationModel

def main():

    i2c_connection: I2cThread = I2cThread()  # Create an Object of the I2cThread class
    k_keypad: KKeypad = KKeypad(i2c_connection)  # Create an Object of the KKeypad class

    k_keypad_qml_presentation_model: KKeypadQmlPresentationModel = KKeypadQmlPresentationModel()  # Create an Object of the KKeypadQmlPresentationModel class

    k_keypad.key_pressed.connect(k_keypad_qml_presentation_model.key_pressed_handler)  # Connect the key_pressed signal of the KKeypad class to the key_pressed_handler slot of the KKeypadQmlPresentationModel class
    k_keypad.key_released.connect(k_keypad_qml_presentation_model.key_released_handler)  # Connect the key_released signal of the KKeypad class to the key_released_handler slot of the KKeypadQmlPresentationModel class

    app: QGuiApplication = QGuiApplication(sys.argv) 
    engine: QQmlApplicationEngine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.rootContext().setContextProperty('kKeypadQmlPresentationModel', k_keypad_qml_presentation_model)  # Make the KKeypadQmlPresentationModel class available to QML
    engine.load('MainWindow.qml')

    i2c_connection.start()  # Start the I2cThread
    # Further Threads can be started here

    app_exit_code: int = app.exec()

    i2c_connection.stop_and_wait() # Stop the I2cThread
    # Further Threads can be stopped here

    sys.exit(app_exit_code)


if __name__ == "__main__":
    main()

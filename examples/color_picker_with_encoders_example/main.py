#!/usr/bin/env python3

import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QTimer

from app_logic import AppLogic

from main_presentation_model import MainPresentationModel
from rotary_encoder_presentation_model import RotaryEncoderPresentationModel


def main():
    # 100 Hz for external timer frequency as default for debouncing the push button signals of the rotary encoders
    DEBOUNCING_EXTERNAL_TIMER_FRQUENCY: int = 100

    main_presentation_model: MainPresentationModel = MainPresentationModel()
    rotary_encoder_presentation_models: list[RotaryEncoderPresentationModel] = [
    ]
    rotary_encoder_index: int
    for rotary_encoder_index in range(4):
        rotary_encoder_presentation_models.append(
            RotaryEncoderPresentationModel())

    app_logic: AppLogic = AppLogic(
        main_presentation_model, rotary_encoder_presentation_models, DEBOUNCING_EXTERNAL_TIMER_FRQUENCY)

    app: QGuiApplication = QGuiApplication(sys.argv)

    engine: QQmlApplicationEngine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.rootContext().setContextProperty(
        'main_presentation_model', main_presentation_model)
    for rotary_encoder_index in range(4):
        engine.rootContext().setContextProperty('rotary_encoder_presentation_model_' +
                                                str(rotary_encoder_index), rotary_encoder_presentation_models[rotary_encoder_index])
    engine.load('./playground/color_picker_with_encoders_example/MainWindow.qml')

    app_logic.setup()

    timer: QTimer = QTimer()
    timer.setInterval(int(1000 / DEBOUNCING_EXTERNAL_TIMER_FRQUENCY))
    timer.timeout.connect(app_logic.timer)
    timer.start()

    app_exit_code: int = app.exec()

    app_logic.cleanup()

    sys.exit(app_exit_code)


if __name__ == "__main__":
    main()

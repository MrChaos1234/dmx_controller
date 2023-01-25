#!/usr/bin/env python3

import sys

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

from stage_view import StageView

from qml_presentation_model_stage_view import StageViewQmlPresentationModel

def main():
    stage_view: StageView = StageView()  # Create an Object of the StageView class

    stage_view_qml_presentation_model: StageViewQmlPresentationModel = StageViewQmlPresentationModel()  # Create an Object of the StageViewQmlPresentationModel class

    stage_view_qml_presentation_model.made_change.connect(stage_view.made_change_handler)  # Connect the model_changend signal of the StageView class to the model_changend_handler slot of the StageViewQmlPresentationModel class
    
    app: QGuiApplication = QGuiApplication(sys.argv) 
    engine: QQmlApplicationEngine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.rootContext().setContextProperty('stageViewQmlPresentationModel', stage_view_qml_presentation_model)  # Make the StageViewQmlPresentationModel class available in QML
    engine.load('MainWindow.qml')

    # Threads can be started here
    
    app_exit_code: int = app.exec()

    # Threads can be stopped here
    
    sys.exit(app_exit_code)


if __name__ == "__main__":
    main()

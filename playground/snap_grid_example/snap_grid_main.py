import sys
import os
import threading
import time

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, QTimer, pyqtSignal


app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load("main_interface/main.qml")

# Main Python code runs here


sys.exit(app.exec_())

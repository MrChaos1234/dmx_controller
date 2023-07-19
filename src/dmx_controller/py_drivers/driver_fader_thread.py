from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot, QThread

# from threading import Thread
from threading import Event
from sys import stdout

from py_drivers.driver_fader_controller_received_bytes_queue import FaderControllerReceivedBytesQueue
from py_drivers.slip_protocol.slip_decoder import SlipDecoder


class FaderControllerDriverThread(QThread):
    WAIT_TIME: float = 0.002

    position_changed: pyqtSignal = pyqtSignal(int, int)  # Qt Signal emitted, if one of the four faders position changes its value in between 0 and 1023

    _stop_event: Event  # event to signal the thread that it should stop
    _fader_controller_received_bytes_queue: FaderControllerReceivedBytesQueue
    _slip_decoder: SlipDecoder

    # _last_positions: list[int]
    # _last_positions_valid: list[bool]

    def __init__(self, fader_controller_received_bytes_queue: FaderControllerReceivedBytesQueue, parent: QObject = None):
        super().__init__(parent)
        self._stop_event = Event()
        self._fader_controller_received_bytes_queue = fader_controller_received_bytes_queue
        self._slip_decoder = SlipDecoder()

        # self._last_positions = [0, 0, 0, 0]
        # self._last_positions_valid = [False, False, False, False]
        # self.dump_file = open("serial-dump2.bin", "wb")

    def run(self) -> None:
        self._stop_event.clear()
        while not self._stop_event.is_set():
            self._receive_bytes()
            sleep(self.WAIT_TIME)

    def _receive_bytes(self) -> None:
        data: bytes = bytes()
        data = self._fader_controller_received_bytes_queue.fetch()
        received_bytes_count: int = 0
        received_bytes_count = len(data)
        if received_bytes_count > 0:
            values: list[dict] = self._slip_decoder.decode(data)
            if len(values) > 0:
                v: dict
                for v in values:
                    if ("fader_index" in v) and ("position" in v):
                        fader_index: int = v["fader_index"]
                        position: int = v["position"]
                        self._notify_position_changed(fader_index, position)

    def _notify_position_changed(self, fader_index: int, position: int) -> None:
        self.position_changed.emit(fader_index, position)

    def stop_and_wait(self) -> None:
        if not self.isFinished:
            # signal the thread to stop
            self._stop_event.set()
            # wait until the thread stopped
            while not self.isFinished:
                sleep(0.01)

            # stdout.write("\n")
            # stdout.flush()
            # self.dump_file.close()

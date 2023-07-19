from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from py_drivers.driver_fader_communication import FaderControllerCommunicationThread
from py_drivers.driver_fader_controller_received_bytes_queue import FaderControllerReceivedBytesQueue
from py_drivers.driver_fader_controller_bytes_to_send_queue import FaderControllerBytesToSendQueue
from py_drivers.driver_fader_thread import FaderControllerDriverThread


class FaderControllerConnection(QObject):
    position_changed: pyqtSignal = pyqtSignal(int, int)  # Qt Signal emitted, if one of the four faders position changes its value in between 0 and 1023

    _received_bytes_queue: FaderControllerReceivedBytesQueue
    _bytes_to_send_queue: FaderControllerBytesToSendQueue
    _communication_thread: FaderControllerCommunicationThread
    _driver_thread: FaderControllerDriverThread

    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self._received_bytes_queue = FaderControllerReceivedBytesQueue()
        self._bytes_to_send_queue = FaderControllerBytesToSendQueue()
        self._communication_thread = FaderControllerCommunicationThread(self._received_bytes_queue, self._bytes_to_send_queue)
        self._driver_thread = FaderControllerDriverThread(self._received_bytes_queue)

    @pyqtSlot(str)
    def setup(self, serial_port_device_name: str) -> None:
        # connect signals of fader hardware instance with slots
        self._driver_thread.position_changed.connect(self._position_changed)
        self._received_bytes_queue.clear()
        self._bytes_to_send_queue.clear()
        self._driver_thread.start()
        self._communication_thread.setup(serial_port_device_name)
        self._communication_thread.start()

    def position_fader(self, fader_index: int, position: int) -> None:
        self._communication_thread.send_fader_position(fader_index, position)

    @pyqtSlot()
    def cleanup(self) -> None:
        try:
            self._driver_thread.position_changed.disconnect()
        except TypeError:
            pass
        self._communication_thread.stop_and_wait()
        self._driver_thread.stop_and_wait()

        # print()
        # if self._communication_thread.chunks_count > 0:
        #     print("last " + str(self._communication_thread.MAX_CHUNK_SIZES_BUFFER_SIZE) + " received chunk sizes:")
        #     chunk_size: int
        #     for chunk_size in self._communication_thread.last_chunk_sizes:
        #         print("  " + str(chunk_size))
        #     print()
        #     print("received " + str(self._communication_thread.chunks_count) + " chunks")
        #     print("min chunk size     = " + str(self._communication_thread.min_chunk_size))
        #     print("max chunk size     = " + str(self._communication_thread.max_chunk_size))
        #     print("average chunk size = " + str(self._communication_thread.chunk_size_sum / self._communication_thread.chunks_count))
        # else:
        #     print("received no chunks!")
        # print()

    @pyqtSlot(int, int)
    def _position_changed(self, fader_index: int, position: int) -> None:
        self._notify_position_changed(fader_index, position)

    def _notify_position_changed(self, fader_index: int, position: int) -> None:
        self.position_changed.emit(fader_index, position)

    @pyqtSlot(int)
    def set_faders_count(self, faders_count: int) -> None:
        self._communication_thread.set_faders_count(faders_count)

    @pyqtSlot(int)
    def set_max_motor_stop_timeout_counter(self, max_motor_stop_timeout_counter: int) -> None:
        self._communication_thread.set_max_motor_stop_timeout_counter(max_motor_stop_timeout_counter)

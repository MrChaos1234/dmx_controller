import sys

from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal, pyqtProperty, pyqtSlot, QThread

# from threading import Thread
from threading import Event
from serial import Serial

from py_drivers.driver_fader_controller_received_bytes_queue import FaderControllerReceivedBytesQueue
from py_drivers.driver_fader_controller_bytes_to_send_queue import FaderControllerBytesToSendQueue
from py_drivers.slip_protocol.slip_packetizer import SlipPacketizer


class FaderControllerCommunicationThread(QThread):
    SLIP_END_CHARACTER: int = 0xC0
    SERIAL_COMMUNICATION_BAUDRATE: int = 115200
    SERIAL_COMMUNICATION_READ_TIMEOUT: float = 0.100
    SERIAL_COMMUNICATION_READ_MAX_CHUNK_SIZE: int = 32
    SERIAL_COMMUNICATION_IGNORE_CHUNKS_AFTER_CONNECT: int = 200

    MAX_CHUNK_SIZES_BUFFER_SIZE: int = 512

    _stop_event: Event  # event to signal the thread that it should stop
    _serial_port: Serial  # serial port
    _serial_port_device_name: str  # name of serial port (e.g. "COM3" or "/dev/ttyUSB0")
    _fader_controller_received_bytes_queue: FaderControllerReceivedBytesQueue
    _fader_controller_bytes_to_send_queue: FaderControllerBytesToSendQueue
    _slip_packetizer: SlipPacketizer

    # min_chunk_size: int
    # max_chunk_size: int
    # chunk_size_sum: int
    # chunks_count: int

    # last_chunk_sizes: list

    def __init__(
        self,
        fader_controller_received_bytes_queue: FaderControllerReceivedBytesQueue,
        fader_controller_bytes_to_send_queue: FaderControllerBytesToSendQueue,
        parent: QObject = None,
    ):
        super().__init__(parent)
        self._stop_event = Event()
        self._serial_port = Serial()
        self._serial_port_device_name = "/dev/ttyUSB0"
        self._fader_controller_received_bytes_queue = fader_controller_received_bytes_queue
        self._fader_controller_bytes_to_send_queue = fader_controller_bytes_to_send_queue
        self._slip_packetizer = SlipPacketizer()

        # self.min_chunk_size = sys.maxsize
        # self.max_chunk_size = 0
        # self.chunk_size_sum = 0
        # self.chunks_count = 0
        # self.last_chunk_sizes = []
        # self.dump_file = open("serial-dump.bin", "wb")
        # self.dump_desc_file = open("serial-dump-desc.txt", "w")

    def setup(self, serial_port_device_name: str) -> None:
        self._serial_port_device_name = serial_port_device_name

    def run(self) -> None:
        self._stop_event.clear()

        self._serial_port.port = self._serial_port_device_name
        self._serial_port.baudrate = self.SERIAL_COMMUNICATION_BAUDRATE
        self._serial_port.timeout = self.SERIAL_COMMUNICATION_READ_TIMEOUT
        self._serial_port.open()
        self._serial_port.reset_input_buffer()

        ignore_chunks_after_connect_counter: int = self.SERIAL_COMMUNICATION_IGNORE_CHUNKS_AFTER_CONNECT

        while not self._stop_event.is_set():
            if ignore_chunks_after_connect_counter > 0:
                # ignore some data from the serial line, because Arduino Nano is rebooting after serial port is opened
                self._serial_port.read(self.SERIAL_COMMUNICATION_READ_MAX_CHUNK_SIZE)
                ignore_chunks_after_connect_counter -= 1
            else:
                self._receive_bytes()
                self._send_bytes()

        self._serial_port.close()

    def _receive_bytes(self) -> None:
        data: bytes = self._serial_port.read(self.SERIAL_COMMUNICATION_READ_MAX_CHUNK_SIZE)
        received_bytes_count: int = len(data)
        if received_bytes_count > 0:
            if not self._fader_controller_received_bytes_queue.add(data):
                self._fader_controller_received_bytes_queue.clear()
                self._fader_controller_received_bytes_queue.add(data)

        # if received_bytes_count > 0:
        #     if received_bytes_count < self.min_chunk_size:
        #         self.min_chunk_size = received_bytes_count
        #     if received_bytes_count > self.max_chunk_size:
        #         self.max_chunk_size = received_bytes_count
        #     self.chunk_size_sum += received_bytes_count
        #     self.chunks_count += 1
        #     self.last_chunk_sizes.append(received_bytes_count)
        #     if len(self.last_chunk_sizes) > self.MAX_CHUNK_SIZES_BUFFER_SIZE:
        #         self.last_chunk_sizes.pop(0)
        #     self.dump_file.write(data)
        #     self.dump_desc_file.write(str(received_bytes_count) + "\n")

    def send_fader_position(self, fader_index: int, position: int) -> None:
        packet: bytes = self._slip_packetizer.packetize_fader_position(fader_index, position)
        self._add_packet_to_send_queue(packet)

    def set_faders_count(self, faders_count: int) -> None:
        packet: bytes = self._slip_packetizer.packetize_faders_count(faders_count)
        self._add_packet_to_send_queue(packet)

    def set_max_motor_stop_timeout_counter(self, max_motor_stop_timeout_counter: int) -> None:
        packet: bytes = self._slip_packetizer.packetize_max_motor_stop_timeout_counter(max_motor_stop_timeout_counter)
        self._add_packet_to_send_queue(packet)

    def _add_packet_to_send_queue(self, packet: bytes) -> None:
        if not self._fader_controller_bytes_to_send_queue.add(packet):
            self._fader_controller_bytes_to_send_queue.clear()
            self._fader_controller_bytes_to_send_queue.add(packet)

    def _send_bytes(self) -> None:
        data: bytes = bytes()
        data = self._fader_controller_bytes_to_send_queue.fetch()
        bytes_to_send_count: int = 0
        bytes_to_send_count = len(data)
        if bytes_to_send_count > 0:
            self._serial_port.write(data)
            self._serial_port.flush()

    def stop_and_wait(self) -> None:
        if not self.isFinished:
            # signal the thread to stop
            self._stop_event.set()
            # wait until the thread stopped
            while not self.isFinished:
                sleep(0.01)

            # self.dump_desc_file.close()
            # self.dump_file.close()

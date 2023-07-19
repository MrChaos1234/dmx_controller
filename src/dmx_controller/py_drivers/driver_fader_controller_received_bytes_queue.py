import queue


class FaderControllerReceivedBytesQueue(object):
    MAX_QUEUE_SIZE: int = 256  # buffers approx. 5 seconds of communication, if data is read in in chunks of 256 Bytes (corresponds approx. 20 ms)

    _received_bytes_queue: queue.Queue  # some thread-safe queue

    def __init__(self):
        self._received_bytes_queue = queue.Queue(self.MAX_QUEUE_SIZE)

    def add(self, received_bytes: bytes) -> bool:
        if not self._received_bytes_queue.full():
            self._received_bytes_queue.put(received_bytes)
            return True
        else:
            return False

    def fetch(self) -> bytes:
        all_received_bytes: bytearray = bytearray()
        while not self._received_bytes_queue.empty():
            all_received_bytes = all_received_bytes + bytearray(self._received_bytes_queue.get())
        return bytes(all_received_bytes)

    def clear(self) -> None:
        while not self._received_bytes_queue.empty():
            self._received_bytes_queue.get()

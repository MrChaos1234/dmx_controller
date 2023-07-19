import queue


class FaderControllerBytesToSendQueue(object):
    MAX_QUEUE_SIZE: int = 32  # buffers approx. 5 'position fader' commands

    _bytes_to_send_queue: queue.Queue  # some thread-safe queue

    def __init__(self):
        self._bytes_to_send_queue = queue.Queue(self.MAX_QUEUE_SIZE)

    def add(self, bytes_to_send: bytes) -> bool:
        if not self._bytes_to_send_queue.full():
            self._bytes_to_send_queue.put(bytes_to_send)
            return True
        else:
            print("FaderControllerBytesToSendQueue.add(): queue is full!")
            return False

    def fetch(self) -> bytes:
        all_bytes_to_send: bytearray = bytearray()
        while not self._bytes_to_send_queue.empty():
            all_bytes_to_send = all_bytes_to_send + bytearray(self._bytes_to_send_queue.get())
        return bytes(all_bytes_to_send)

    def clear(self) -> None:
        while not self._bytes_to_send_queue.empty():
            self._bytes_to_send_queue.get()

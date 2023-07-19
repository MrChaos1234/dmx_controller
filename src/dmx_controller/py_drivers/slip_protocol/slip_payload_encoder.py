class SlipPayloadEncoder:
    SLIP_END_CHARACTER: int = 0xC0
    SLIP_ESC_CHARACTER: int = 0xDB
    SLIP_ESCAPE_END_CHARACTER: int = 0xDC
    SLIP_ESCAPE_ESC_CHARACTER: int = 0xDD

    def __init__(self):
        pass

    def encode(self, payload: bytes) -> bytes:
        encoded_payload: bytearray = bytearray()

        if len(payload) > 0:
            byte: int
            for byte in payload:
                encoded_payload.extend(self._encode_char(byte))

        return bytes(encoded_payload)

    def _encode_char(self, char: int) -> bytearray:
        if char == self.SLIP_ESC_CHARACTER:
            return bytearray([self.SLIP_ESC_CHARACTER, self.SLIP_ESCAPE_ESC_CHARACTER])
        elif char == self.SLIP_END_CHARACTER:
            return bytearray([self.SLIP_ESC_CHARACTER, self.SLIP_ESCAPE_END_CHARACTER])
        else:
            return bytearray([char])

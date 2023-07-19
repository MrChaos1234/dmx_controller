class SlipPayloadDecoder:
    SLIP_END_CHARACTER: int = 0xC0
    SLIP_ESC_CHARACTER: int = 0xDB
    SLIP_ESCAPE_END_CHARACTER: int = 0xDC
    SLIP_ESCAPE_ESC_CHARACTER: int = 0xDD

    def __init__(self):
        pass

    def decode(self, payload: bytes) -> dict:
        decoded_payload: bytearray = bytearray()

        if len(payload) > 0:
            if len(payload) > 1:
                payload_index: int = 0
                while payload_index < len(payload):
                    if payload[payload_index] != self.SLIP_ESC_CHARACTER:
                        decoded_payload.append(payload[payload_index])
                        payload_index = payload_index + 1
                    else:
                        if payload_index < len(payload) - 1:
                            decoded_payload.append(self._decode_char(payload, payload_index))
                            payload_index = payload_index + 2
                        else:
                            payload_index = payload_index + 1
            else:
                if payload[0] != self.SLIP_ESC_CHARACTER:
                    decoded_payload.append(payload[0])
        return bytes(decoded_payload)

    def _decode_char(self, payload: bytes, payload_index: int) -> int:
        if payload[payload_index + 1] == self.SLIP_ESCAPE_END_CHARACTER:
            return self.SLIP_END_CHARACTER
        else:
            return self.SLIP_ESC_CHARACTER

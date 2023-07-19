from .slip_payload_encoder import SlipPayloadEncoder


class SlipPacketizer:
    SLIP_END_CHARACTER: int = 0xC0
    CMD_SET_FADERS_COUNT: int = 0x1
    CMD_SET_MAX_MOTOR_STOP_TIMEOUT_COUNTER: int = 0x2

    _slip_payload_encoder: SlipPayloadEncoder

    def __init__(self):
        self._slip_payload_encoder = SlipPayloadEncoder()

    def packetize_fader_position(self, fader_index: int, position: int) -> bytes:
        packet_to_return: bytearray = bytearray()
        packet_to_return.append(self.SLIP_END_CHARACTER)
        packet_to_return.extend(bytearray(self._create_fader_position_payload(fader_index, position)))
        packet_to_return.append(self.SLIP_END_CHARACTER)
        return bytes(packet_to_return)

    def _create_fader_position_payload(self, fader_index: int, position: int) -> bytes:
        high_byte: int = (fader_index << 6) + (position >> 8)
        low_byte: int = position & 0xFF
        return self._slip_payload_encoder.encode(bytes([high_byte, low_byte]))

    def packetize_faders_count(self, faders_count: int) -> bytes:
        packet_to_return: bytearray = bytearray()
        packet_to_return.append(self.SLIP_END_CHARACTER)
        packet_to_return.extend(bytearray(self._create_faders_count_payload(faders_count)))
        packet_to_return.append(self.SLIP_END_CHARACTER)
        return bytes(packet_to_return)

    def _create_faders_count_payload(self, faders_count: int) -> bytes:
        high_byte: int = self.CMD_SET_FADERS_COUNT << 2
        low_byte: int = faders_count
        return self._slip_payload_encoder.encode(bytes([high_byte, low_byte]))

    def packetize_max_motor_stop_timeout_counter(self, max_motor_stop_timeout_counter: int) -> bytes:
        packet_to_return: bytearray = bytearray()
        packet_to_return.append(self.SLIP_END_CHARACTER)
        packet_to_return.extend(bytearray(self._create_max_motor_stop_timeout_counter_payload(max_motor_stop_timeout_counter)))
        packet_to_return.append(self.SLIP_END_CHARACTER)
        return bytes(packet_to_return)

    def _create_max_motor_stop_timeout_counter_payload(self, max_motor_stop_timeout_counter: int) -> bytes:
        high_byte: int = self.CMD_SET_MAX_MOTOR_STOP_TIMEOUT_COUNTER << 2
        low_byte: int = max_motor_stop_timeout_counter
        return self._slip_payload_encoder.encode(bytes([high_byte, low_byte]))

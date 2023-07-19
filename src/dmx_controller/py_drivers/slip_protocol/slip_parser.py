from .slip_token_type import SlipTokenType
from .slip_payload_decoder import SlipPayloadDecoder


class SlipParser:
    SLIP_END_CHARACTER: int = 0xC0
    SLIP_ESC_CHARACTER: int = 0xDB
    SLIP_ESCAPE_END_CHARACTER: int = 0xDC
    SLIP_ESCAPE_ESC_CHARACTER: int = 0xDD

    _tokens: list[dict]
    _slip_payload_decoder: SlipPayloadDecoder

    def __init__(self):
        self._tokens = []
        self._slip_payload_decoder = SlipPayloadDecoder()

    def add(self, tokens: list[dict]) -> None:
        self._tokens = self._tokens + tokens

    def parse(self) -> list[dict]:
        values_to_return: list[dict] = []
        token_index: int = 0
        while token_index < (len(self._tokens) - 2):
            token: dict = self._tokens[token_index]
            # search for first <END> token
            if token["type"] == SlipTokenType.END_CHAR_TOKEN:
                # first <END> token found

                # search for second <END> token
                second_token_index: int = token_index + 1
                while second_token_index < len(self._tokens):
                    token: dict = self._tokens[second_token_index]
                    # search for second <END> token
                    if token["type"] == SlipTokenType.END_CHAR_TOKEN:
                        # second <END> token found

                        if (second_token_index - token_index) == 2:
                            # payload surrounded by two <END> tokens found

                            # pack payload into list of parsed values
                            self._add_value(values_to_return, token_index + 1)
                            self._tokens = self._tokens[second_token_index + 1 :]
                            token_index = 0
                            break
                        else:
                            # sequence of <END> tokens and payload is wrong, so discard all tokens in front of the second <END> token
                            self._tokens = self._tokens[second_token_index:]
                            token_index = 0
                            break
                    second_token_index = second_token_index + 1

                continue
            token_index = token_index + 1
        return values_to_return

    def _add_value(self, values: list[dict], token_index: int) -> None:
        payload_token: dict = self._tokens[token_index]
        data: bytes = payload_token["data"]
        value: dict = self._convert_payload(data)
        values.append(value)

    def _convert_payload(self, payload: bytes) -> dict:
        if len(payload) > 1:
            decoded_payload: bytes = self._slip_payload_decoder.decode(payload)
            if len(decoded_payload) == 2:
                return self._convert_decoded_payload(decoded_payload)
        return {}

    def _convert_decoded_payload(self, decoded_payload) -> dict:
        value_to_return: dict = {"fader_index": 0, "position": 0}
        high_byte: int = decoded_payload[0]
        fader_index: int = high_byte >> 6
        value_to_return["fader_index"] = fader_index
        high_byte = high_byte & 0x3F
        low_byte: int = decoded_payload[1]
        position: int = (high_byte << 8) + low_byte
        value_to_return["position"] = position
        return value_to_return

    # for testing
    def get_tokens(self) -> list[dict]:
        return self._tokens

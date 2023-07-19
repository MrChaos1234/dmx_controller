from .slip_token_type import SlipTokenType


class SlipTokenizer:
    SLIP_END_CHARACTER = 0xC0

    _data: bytes

    def __init__(self):
        self._data = bytes()

    def add(self, data: bytes) -> None:
        self._data = self._data + data

    def find_tokens(self) -> list[dict]:
        tokens_to_return: list[dict] = []
        data_index: int = 0
        while data_index < len(self._data):
            if self._data[data_index] == self.SLIP_END_CHARACTER:
                # character <END> found

                # pack data before <END> into data token
                self._add_data_token(tokens_to_return, data_index)
                # pack <END> into token
                self._add_end_char_token(tokens_to_return)
                self._data = self._data[data_index + 1 :]
                data_index = 0
                continue
            data_index = data_index + 1
        return tokens_to_return

    def _add_data_token(self, tokens: list[dict], data_index: int) -> None:
        if data_index > 0:
            payload_token: dict = {
                "type": SlipTokenType.PAYLOAD_TOKEN,
                "data": self._data[:data_index],
            }
            tokens.append(payload_token)

    def _add_end_char_token(self, tokens: list[dict]) -> None:
        end_char_token: dict = {"type": SlipTokenType.END_CHAR_TOKEN}
        tokens.append(end_char_token)

    # for testing
    def get_data(self) -> bytes:
        return self._data

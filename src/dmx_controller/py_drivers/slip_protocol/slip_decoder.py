from .slip_tokenizer import SlipTokenizer
from .slip_parser import SlipParser


class SlipDecoder:
    SLIP_END_CHARACTER = 0xC0

    _tokenizer: SlipTokenizer
    _slip_parser: SlipParser

    def __init__(self):
        self._tokenizer = SlipTokenizer()
        self._slip_parser = SlipParser()

    def decode(self, data: bytes) -> list[dict]:
        result: list[dict] = []
        if len(data) > 0:
            self._tokenizer.add(data)
            tokens: list[dict] = self._tokenizer.find_tokens()
            if len(tokens) > 0:
                self._slip_parser.add(tokens)
                result = self._slip_parser.parse()
        return result

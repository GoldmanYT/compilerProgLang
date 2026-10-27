from typing import Iterable

from tokens import Token


class Sct:
    """
    Syntactically controlled translation
    """

    def __init__(self, tokens: Iterable[Token]):
        self.tokens: Iterable = tokens

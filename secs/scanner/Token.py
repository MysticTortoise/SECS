from typing import Any

from secs.Value import SECSValue
from secs.scanner.TokenType import TokenType

class Token:
    type: TokenType
    lexeme: str
    literal: SECSValue
    line: int

    def __init__(self, type: TokenType, lexeme: str, literal: Any, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"
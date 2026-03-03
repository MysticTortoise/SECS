from enum import Enum, auto


class TokenType(Enum):
    # SINGLE CHAR TOKENS

    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()

    COMMA = auto()
    DOT = auto()
    SEMICOLON = auto()
    NUMBER_SIGN = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()

    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER_EQUAL = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    LESS = auto()

    IDENTIFIER = auto()
    NUMBER = auto()


    EOF = auto()

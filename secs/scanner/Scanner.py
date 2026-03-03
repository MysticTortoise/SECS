from typing import Any

from secs.Value import SECSValue
from secs.scanner.Token import Token
from secs.scanner.TokenType import TokenType

source: str

start: int
current: int
line: int

tokens: list[Token]

def scan_tokens(codeSource: str):
    source = codeSource

    start = 0
    current = 0
    line = 1

    while not _is_at_end():
        start = current
        _scan_token()

    tokens.append(Token(TokenType.EOF, "", None), line)


# Scanning Functions

def _is_at_end() -> bool:
    return current >= len(source)

def _advance() -> str:
    global current
    current = current + 1
    return source[current-1]

def _peek() -> str:
    if(_is_at_end()):
        return "\0"

    return source[current]

def _peek_ahead(amount: int) -> str:
    if(current + amount) >= len(source):
        return "\0"
    return source[current + amount]

def _match(expected: str) -> bool:
    if _peek() != expected:
        return False

    global current
    current = current + 1
    return True

# Add token functions
def _add_token(type : TokenType, literal: SECSValue):
    text: str = source[start:current]
    tokens.append(Token(type, text, literal, line))

def _add_token(type: TokenType):
    _add_token(type, None)



def _scan_token():
    c:str = _advance()

    if c == "(":
        _add_token(TokenType.LEFT_PAREN)
        return
    elif c == ")":
        _add_token(TokenType.RIGHT_PAREN)
        return
    elif c == ",":
        _add_token(TokenType.COMMA)
        return
    elif c == ".":
        _add_token(TokenType.DOT)
        return
    elif c == ";":
        _add_token(TokenType.SEMICOLON)
        return
    elif c == "+":
        _add_token(TokenType.PLUS)
        return
    elif c == "-":
        _add_token(TokenType.MINUS)
        return
    elif c == "*":
        _add_token(TokenType.STAR)
        return
    elif c == "/":
        _add_token(TokenType.SLASH)
        return
    elif c == "#":
        while _peek() != "\n" and not _is_at_end():
            _advance()
        return

    elif c == "!":
        _add_token(TokenType.BANG_EQUAL if _match("=") else TokenType.BANG)
        return
    elif c == ">":
        _add_token(TokenType.GREATER_EQUAL if _match("=") else TokenType.GREATER)
        return
    elif c == "<":
        _add_token(TokenType.LESS_EQUAL if _match("=") else TokenType.LESS)
        return
    elif c == "=":
        _add_token(TokenType.EQUAL_EQUAL if _match("=") else TokenType.EQUAL)
        return

    elif c == "\n":
        global line
        line = line + 1
        return
    elif c == " " or c == "\r" or c == "\t":
        return


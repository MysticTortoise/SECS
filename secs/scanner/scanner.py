from secs.Value import SECSValue
from secs.error.error import error
from secs.scanner.Token import Token
from secs.scanner.TokenType import TokenType

source: str

start: int
current: int
line: int

tokens: list[Token]

def scan_tokens(code_source: str) -> list[Token]:
    global source, start, current, line, tokens

    source = code_source

    start = 0
    current = 0
    line = 1

    tokens = list()

    while not _is_at_end():
        start = current
        _scan_token()

    tokens.append(Token(TokenType.EOF, "", None, line))
    return tokens


# Scanning Functions

def _is_at_end() -> bool:
    return current >= len(source)

def _advance() -> str:
    global current
    current = current + 1
    return source[current-1]

def _peek() -> str:
    if _is_at_end():
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
def _add_token(type : TokenType, literal: SECSValue = None):
    text: str = source[start:current]
    tokens.append(Token(type, text, literal, line))


# Categorical Functions
def _is_digit(c : str):
    return c in "0123456789"

def _is_alpha(c : str):
    n = ord(c)
    return (ord('a') < n < ord('z')) or (ord('A') < n < ord('Z')) or n == ord('_')

def _is_alphanumeric(c: str):
    return _is_alpha(c) or _is_digit(c)

def _scan_token():
    global line

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
        line = line + 1
        return
    elif c == " " or c == "\r" or c == "\t":
        return

    if _is_digit(c):
        _scan_number_literal()
        return

    if _is_alpha(c):
        _scan_identifier()
        return

    error(line, f"Unexpected character {c}.")



def _scan_number_literal():
    while _is_digit(_peek()):
        _advance()

    if _peek() == "." and _is_digit(_peek_ahead(1)):
        _advance()

        while _is_digit(_peek()):
            _advance()

    _add_token(TokenType.NUMBER, float(source[start:current]))

def _scan_identifier():
    while _is_alphanumeric(_peek()):
        _advance()

    # future shiz if keywords get added
    #text = source[start:current]
    #type = TokenType.IDENTIFIER

    _add_token(TokenType.IDENTIFIER)


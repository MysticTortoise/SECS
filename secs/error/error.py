import sys

from secs.scanner.Token import Token
from secs.scanner.TokenType import TokenType

had_error : bool = False

def _report_error(line: int, where: str, message: str):
    global had_error
    print(f"[line {line}] Error {where}: {message}", file=sys.stderr)
    had_error = True



def _error_int(line: int, message: str):
    _report_error(line, "", message)

def _error_token(token: Token, message: str):
    if token.type == TokenType.EOF:
        _report_error(token.line, " at end", message)
    else:
        _report_error(token.line, f" at '{token.lexeme}'", message)

def error(a, message: str):
    if isinstance(a, Token):
        _error_token(a, message)
    elif isinstance(a, int):
        _error_int(a, message)
    else:
        raise ValueError("error(a, message) called with incorrect type!")
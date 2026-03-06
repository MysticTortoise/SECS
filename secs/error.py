import sys

from secs.scanner.Token import Token
from secs.scanner.TokenType import TokenType


def _report_error(line: int, where: str, message: str):
    print(f"[line {line}] Error {where}: {message}", file=sys.stderr)


def _error_int(line: int, message: str):
    _report_error(line, "", message)

def _error_token(token: Token, message: str):
    if token.type == TokenType.EOF:
        _report_error(token.line, " at end", message)
    else:
        _report_error(token.line, f" at '{token.lexeme}'", message)

def error(a, message: str):
    if a is Token:
        _error_token(a, message)
    elif a is int:
        _error_int(a, message)
    else:
        raise ValueError("error(a, message) called with incorrect type!")
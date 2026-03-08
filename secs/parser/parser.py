from secs.error.EvalError import EvalError
from secs.error.ParseError import ParseError
from secs.error.error import error
from secs.parser.Expression import *
from secs.parser.Statement import Statement
from secs.scanner.Token import Token
from secs.scanner.TokenType import TokenType

_tokens: list[Token]
_current: int

def parse_tokens(tokens: list[Token]) -> list[Statement]:
    global _tokens, _current

    _tokens = tokens
    _current = 0

    statements: list[Statement] = list()

    while not _is_at_end():
        try:
            statements.append(_statement())
        except ParseError:
            _advance()
            while not _is_at_end():
                if _previous().type == TokenType.SEMICOLON:
                    break
                _advance()
        

    return statements


def _peek() -> Token:
    return _tokens[_current]

def _previous() -> Token:
    return _tokens[_current - 1]

def _is_at_end() -> bool:
    return _peek().type == TokenType.EOF

def _advance() -> Token:
    global _current

    if not _is_at_end():
        _current = _current + 1

    return _previous()

def _check(type: TokenType) -> bool:
    if _is_at_end():
        return False
    return _peek().type == type

def _match(*types: TokenType) -> bool:
    for type in types:
        if _check(type):
            _advance()
            return True
    return False

def _consume(type: TokenType, message: str) -> Token:
    if _check(type):
        return _advance()

    raise _error(_peek(), message)

def _error(token: Token, message: str) -> ParseError:
    error(token, message)
    return ParseError(message)


def _statement() -> Statement:
    name = _consume(TokenType.IDENTIFIER, "Expected expression name!")

    params = list()
    if _match(TokenType.LEFT_PAREN):
        while True:
            params.append(_consume(TokenType.IDENTIFIER, "Expected parameter name."))
            if not _match(TokenType.COMMA):
                break
        _consume(TokenType.RIGHT_PAREN, "Expected ')' to match '(' in function-expression definition.")

    _consume(TokenType.EQUAL, "Expected '=' symbol to come after expression name!")

    expression = _expression()
    _consume(TokenType.SEMICOLON, "Expected ';' after expression!")

    return Statement(name, expression, params)


# Expression Parsing ===========================================================
def _expression() -> Expression:
    return _e_ternary()

def _e_ternary() -> Expression:
    expr = _e_equality()

    while _match(TokenType.QUESTION):
        left_op = _previous()
        middle = _e_equality()
        right_op = _consume(TokenType.COLON, "Expected : after expression!")
        right = _e_equality()

        expr = TernaryExpr(expr, left_op, middle, right_op, right)

    return expr

def _e_equality() -> Expression:
    expr = _e_comparison()

    while _match(TokenType.EQUAL_EQUAL, TokenType.BANG_EQUAL):
        operator = _previous()
        right = _e_comparison()

        expr = BinaryExpr(expr, operator, right)

    return expr

def _e_comparison() -> Expression:
    expr = _e_term()

    while _match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
        operator = _previous()
        right = _e_term()

        expr = BinaryExpr(expr, operator, right)

    return expr

def _e_term() -> Expression:
    expr = _e_factor()

    while _match(TokenType.PLUS, TokenType.MINUS):
        operator = _previous()
        right = _e_factor()

        expr = BinaryExpr(expr, operator, right)

    return expr

def _e_factor() -> Expression:
    expr = _e_unary()

    while _match(TokenType.STAR, TokenType.SLASH):
        operator = _previous()
        right = _e_unary()

        expr = BinaryExpr(expr, operator, right)

    return expr

def _e_unary() -> Expression:
    if _match(TokenType.MINUS, TokenType.BANG):
        operator = _previous()
        right_expr = _e_unary()
        return UnaryExpr(operator, right_expr)

    return _e_primary()

def _e_primary() -> Expression:
    if _match(TokenType.NUMBER):
        return LiteralExpr(_previous().literal)
    if _match(TokenType.IDENTIFIER):
        identifier = _previous()
        if _match(TokenType.LEFT_PAREN):
            return _e_call(identifier)
        else:
            return IdentifierExpr(identifier)

    if _match(TokenType.LEFT_PAREN):
        expression = _expression()
        _consume(TokenType.RIGHT_PAREN, "Expected ')' after expression to match ')'.")
        return GroupingExpr(expression)

    raise _error(_peek(), "Expected expression.")

def _e_call(identifier: Token):
    arguments = list()
    while True:
        arguments.append(_expression())
        if not _match(TokenType.COMMA):
            break

    paren = _consume(TokenType.RIGHT_PAREN, "Expected ')' after arguments.")

    return CallExpr(identifier, paren, arguments)
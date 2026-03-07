from secs.error.ParseError import ParseError
from secs.error.error import error
from secs.parser.Expression import *
from secs.parser.ExpressionDeclaration import ExpressionDeclaration
from secs.scanner.Token import Token
from secs.scanner.TokenType import TokenType

_tokens: list[Token]
_current: int

def parse_tokens(tokens: list[Token]) -> list[ExpressionDeclaration]:
    global _tokens, _current

    _tokens = tokens
    _current = 0

    statements: list[ExpressionDeclaration] = list()

    while not _is_at_end():
        statements.append(_statement())

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
    return ParseError()


def _statement() -> ExpressionDeclaration:
    name = _consume(TokenType.IDENTIFIER, "Expected expression name!")
    _consume(TokenType.EQUAL, "Expected '=' symbol to come after expression name!")

    expression = _expression()
    _consume(TokenType.SEMICOLON, "Expected ';' after expression!")

    return ExpressionDeclaration(name, expression)


# Expression Parsing ===========================================================
def _expression() -> Expression:
    return _e_ternary()

def _e_ternary() -> Expression:
    expr = _e_equality()

    while(_match(TokenType.QUESTION)):
        leftOp = _previous()
        middle = _e_equality()
        rightOp = _consume(TokenType.COLON, "Expected : after expression!")
        right = _e_equality()

        expr = TernaryExpr(expr, leftOp, middle, rightOp, right)

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
    if _match(TokenType.MINUS):
        operator = _previous()
        rightExpr = _e_unary()
        return UnaryExpr(operator, rightExpr)

    return _e_primary()

def _e_primary() -> Expression:
    if _match(TokenType.NUMBER):
        return LiteralExpr(_previous().literal)
    if _match(TokenType.IDENTIFIER):
        return IdentifierExpr(_previous())
    if _match(TokenType.LEFT_PAREN):
        expression = _expression()
        _consume(TokenType.RIGHT_PAREN, "Expected ')' after expression to match ')'.")
        return GroupingExpr(expression)

    raise _error(_peek(), "Expected expression.")

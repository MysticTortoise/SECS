from secs.parser.Expression import Expression
from secs.scanner.Token import Token


class Statement:
    name: Token
    arguments: list[Token] | None
    expression: Expression

    def __init__(self, name: Token, expression: Expression, arguments: list[Token] | None):
        self.name = name
        self.expression = expression
        self.arguments = arguments

    def __str__(self):
        return f"{self.name.lexeme} - [{self.expression}]"
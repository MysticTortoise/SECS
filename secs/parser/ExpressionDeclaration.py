from typing import Any

from secs.scanner.Token import Token


class ExpressionDeclaration:
    name: Token
    expression: Any

    def __init__(self, name: Token, expression):
        self.name = name
        self.expression = expression

    def __str__(self):
        return f"{self.name.lexeme} - [{self.expression}]"
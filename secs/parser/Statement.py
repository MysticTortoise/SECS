from secs.parser.Expression import Expression
from secs.scanner.Token import Token


class Statement:
    name: Token
    expression: Expression

    def __init__(self, name: Token, expression: Expression):
        self.name = name
        self.expression = expression

    def __str__(self):
        return f"{self.name.lexeme} - [{self.expression}]"
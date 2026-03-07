from abc import ABC

from secs.Value import SECSValue
from secs.scanner.Token import Token


class Expression(ABC):
    pass


class LiteralExpr(Expression):
    value: SECSValue

    def __init__(self, value: SECSValue):
        self.value = value

class IdentifierExpr(Expression):
    name: Token

    def __init__(self, token: Token):
        self.name = token

class GroupingExpr(Expression):
    expression: Expression

    def __init__(self, expression:Expression):
        self.expression = expression

class UnaryExpr(Expression):
    operator: Token
    right: Expression

    def __init__(self, operator:Token, right:Expression):
        self.operator = operator
        self.right = right

from abc import ABC

from secs.Value import SECSValue
from secs.scanner.Token import Token


class Expression(ABC):
    pass


class LiteralExpr(Expression):
    value: SECSValue

    def __init__(self, value: SECSValue):
        self.value = value

    def __str__(self):
        return f"{self.value}"

class IdentifierExpr(Expression):
    name: Token

    def __init__(self, token: Token):
        self.name = token

    def __str__(self):
        return f"{self.name.lexeme}"

class GroupingExpr(Expression):
    expression: Expression

    def __init__(self, expression:Expression):
        self.expression = expression

    def __str__(self):
        return f"({self.expression})"

class UnaryExpr(Expression):
    operator: Token
    right: Expression

    def __init__(self, operator:Token, right:Expression):
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"{self.operator.lexeme}{self.right}"

class BinaryExpr(Expression):
    left: Expression
    operator: Token
    right:Expression

    def __init__(self, left:Expression, operator:Token, right:Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"{self.left} {self.operator.lexeme} {self.right}"

class TernaryExpr(Expression):
    left: Expression
    left_op: Token
    middle:Expression
    right_op: Token
    right: Expression

    def __init__(self, left:Expression, left_op:Token, middle:Expression, right_op:Token, right:Expression):
        self.left = left
        self.left_op = left_op
        self.middle = middle
        self.right_op = right_op
        self.right = right

    def __str__(self):
        return f"{self.left} {self.left_op.lexeme} {self.middle} {self.right_op} {self.right}"
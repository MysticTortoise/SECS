from ..error.EvalError import EvalError
from ..parser.Expression import *
from ..parser.Statement import Statement
from ..scanner.TokenType import TokenType

from .SECSContext import SECSContext


def evaluate_statement(name: str, context: SECSContext) -> SECSValue:
    if not (name in context.statements.keys()):
        if context.parent is None:
            raise EvalError(f"{name} is not a valid expression!")
        else:
            return evaluate_statement(name, context.parent)

    if name in context.visited_statements:
        raise EvalError(f"Recursive call of {name} detected!")

    statement = context.statements[name]
    # len(statement.arguments) != len(arguments):
        #raise EvalError(f"Invalid arguments for function expression! Expected {len(statement.arguments)} arguments but got {len(arguments)}.")

    context.visited_statements.append(name)
    val = _evaluate_statement(statement, context)
    context.visited_statements.pop()

    return val

def _evaluate_statement(statement: Statement, context: SECSContext) -> SECSValue:
    return _evaluate_expression(statement.expression, context)

def _evaluate_expression(expression: Expression, context: SECSContext) -> SECSValue:
    if isinstance(expression, TernaryExpr):
        return _eval_ternary(expression, context)
    if isinstance(expression, BinaryExpr):
        return _eval_binary(expression, context)
    if isinstance(expression, UnaryExpr):
        return _eval_unary(expression, context)
    if isinstance(expression, GroupingExpr):
        return _eval_grouping(expression, context)
    if isinstance(expression, IdentifierExpr):
        return _eval_identifier(expression, context)
    if isinstance(expression, CallExpr):
        return _eval_call(expression, context)
    if isinstance(expression, LiteralExpr):
        return _eval_literal(expression)

    raise EvalError("Unknown expression type.")

def _is_truthy(val: SECSValue) -> bool:
    return val != 0

def _eval_ternary(expr: TernaryExpr, context: SECSContext):
    if _is_truthy(_evaluate_expression(expr.left, context)):
        return _evaluate_expression(expr.middle, context)
    else:
        return _evaluate_expression(expr.right, context)

def _eval_binary(expr: BinaryExpr, context: SECSContext):
    left = _evaluate_expression(expr.left, context)
    right = _evaluate_expression(expr.right, context)

    if expr.operator.type == TokenType.PLUS:
        return left + right
    if expr.operator.type == TokenType.MINUS:
        return left - right
    if expr.operator.type == TokenType.STAR:
        return left * right
    if expr.operator.type == TokenType.SLASH:
        return left / right

    if expr.operator.type == TokenType.GREATER:
        return 1 if left > right else 0
    if expr.operator.type == TokenType.GREATER_EQUAL:
        return 1 if left >= right else 0
    if expr.operator.type == TokenType.LESS:
        return 1 if left < right else 0
    if expr.operator.type == TokenType.LESS_EQUAL:
        return 1 if left <= right else 0

    if expr.operator.type == TokenType.EQUAL_EQUAL:
        return 1 if left == right else 0
    if expr.operator.type == TokenType.BANG_EQUAL:
        return 1 if left != right else 0

    raise EvalError(f"Unknown binary operator {expr.operator.lexeme}")

def _eval_unary(expr: UnaryExpr, context: SECSContext) -> SECSValue:
    if expr.operator.type == TokenType.MINUS:
        return -(_evaluate_expression(expr.right, context))
    if expr.operator.type == TokenType.BANG:
        val = _evaluate_expression(expr.right, context)
        return val if _is_truthy(val) else 0

    raise EvalError(f"Unknown unary operator {expr.operator.lexeme}")



def _eval_grouping(expr: GroupingExpr, context: SECSContext) -> SECSValue:
    return _evaluate_expression(expr.expression, context)

def _eval_identifier(expr: IdentifierExpr, context: SECSContext) -> SECSValue:
    return evaluate_statement(expr.name.lexeme, context)

def _eval_call(expr: CallExpr, context: SECSContext) -> SECSValue:
    calling_statement = context.get_statement(expr.callee.lexeme)
    sub_context = SECSContext([context.get_statement(calling_statement.name.lexeme)], context)

    for i in range(len(expr.args)):
        arg_name = calling_statement.arguments[i]
        arg_statement = Statement(arg_name,expr.args[i], list())
        sub_context.add_statement(arg_statement)

    return evaluate_statement(calling_statement.name.lexeme, sub_context)



def _eval_literal(expr: LiteralExpr) -> SECSValue:
    return expr.value
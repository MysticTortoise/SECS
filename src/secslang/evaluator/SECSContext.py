from ..Value import SECSValue
from ..error.EvalError import EvalError
from ..error.NoStatementError import NoStatementError
from ..parser.Statement import Statement

class SECSContext:
    parent: SECSContext | None
    statements: dict[str, Statement]
    visited_statements = []

    def __init__(self, statements: list[Statement], parent: SECSContext | None):
        self.statements = dict()
        self.parent = parent
        self.add_statements(statements)

    def add_statement(self, statement: Statement):
        if statement.name in self.statements.keys():
            raise EvalError("Attempt to redefine a statement!")
        self.statements[statement.name.lexeme] = statement

    def add_statements(self, statements: list[Statement]):
        for statement in statements:
            self.add_statement(statement)

    def get_statement(self, name: str):
        if name in self.statements.keys():
            return self.statements[name]
        if self.parent is None:
            return None
        return self.parent.get_statement(name)


    def eval_statement(self, name: str) -> SECSValue:
        from .evaluator import evaluate_statement
        return evaluate_statement(name, self)

    def eval_statement_default(self, name: str, default: SECSValue) -> SECSValue:
        try:
            return self.eval_statement(name)
        except NoStatementError:
            return default

    def print_all_statements(self):
        for statement in self.statements.values():
            if len(statement.arguments) > 0:
                continue
            print(f"{statement.name.lexeme} - {self.eval_statement(statement.name.lexeme)}")

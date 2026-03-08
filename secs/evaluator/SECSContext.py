from secs.Value import SECSValue
from secs.error.EvalError import EvalError
from secs.parser.Statement import Statement

class SECSContext:
    statements: dict[str, Statement]
    visited_statements = []

    def __init__(self, statements: list[Statement]):
        self.statements = dict()
        self.add_statements(statements)

    def add_statement(self, statement: Statement):
        if statement.name in self.statements.keys():
            raise EvalError("Attempt to redefine a statement!")
        self.statements[statement.name.lexeme] = statement

    def add_statements(self, statements: list[Statement]):
        for statement in statements:
            self.add_statement(statement)

    def eval_statement(self, name: str) -> SECSValue:
        from secs.evaluator.evaluator import evaluate_statement
        return evaluate_statement(name, self)

    def print_all_statements(self):
        for statement in self.statements.keys():
            print(self.eval_statement(statement))

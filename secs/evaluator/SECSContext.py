from secs.parser.Statement import Statement

class SECSContext:
    statements: dict[str, Statement]
    visited_statements = []

    def __init__(self, statements: dict[str,Statement]):
        self.statements = statements


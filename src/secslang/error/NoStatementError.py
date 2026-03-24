class NoStatementError(Exception):
    def __init__(self, statement_name: str):
        super().__init__(f"SECS Error: {statement_name} is not an expression!")
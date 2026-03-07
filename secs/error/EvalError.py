class EvalError(Exception):
    def __init__(self, message):
        super().__init__(f"Evaluation Error: {message}")
class CodeIssue:
    def __init__(self, line: int, code: str, message: str):
        self.line = line + 1
        self.code = code
        self.message = message

    def __str__(self):
        return f"Line {self.line}: {self.code} {self.message}"

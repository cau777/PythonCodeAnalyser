from _ast import expr
from ast import FunctionDef, ClassDef, Constant, Assign, Name
from code_issue import CodeIssue
import ast
import re

snake_case_regex = "[a-z\\d_]+"


class NodeChecker(ast.NodeVisitor):
    def __init__(self):
        self.issues: list[CodeIssue] = []
        self.is_func = False

    def visit_FunctionDef(self, node: FunctionDef):
        func_name = node.name
        line = node.lineno - 1
        if not re.match(snake_case_regex, func_name):
            self.issues.append(CodeIssue(line, "S009", f"Function name '{func_name}' should use snake_case"))

        for arg in node.args.args:
            name = arg.arg
            if not re.match(snake_case_regex, name):
                self.issues.append(CodeIssue(line, "S010", f"Argument name '{name}' should be snake_case"))

        for default in node.args.defaults:
            if not type(default) == Constant:
                self.issues.append(CodeIssue(line, "S012", "Default argument value is mutable"))

        self.is_func = True
        self.generic_visit(node)
        self.is_func = False

    def visit_ClassDef(self, node: ClassDef):
        classname = node.name
        line = node.lineno - 1
        if not re.match("[A-Z][A-Za-z\\d]", classname):
            self.issues.append(CodeIssue(line, "S008", f"Class name '{classname}' should use CamelCase"))

        self.generic_visit(node)

    def visit_Assign(self, node: Assign):
        if not self.is_func:
            return

        for target in node.targets:
            if type(target) == Name:
                target: Name
                line = target.lineno - 1
                if not re.match(snake_case_regex, target.id):
                    self.issues.append(
                        CodeIssue(line, "S011", f"Variable '{target.id}' in function should be snake_case"))

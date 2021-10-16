from node_checker import NodeChecker
from code_issue import CodeIssue
import os.path
import re
import argparse
import os
import os.path
import glob
import ast

path = ""


def parse_args():
    global path

    parser = argparse.ArgumentParser()
    parser.add_argument("path")

    args = parser.parse_args()
    path = args.path


def read_file(filepath: str):
    with open(filepath, "r") as f:
        return f.read()


def find_comment(line: str):
    return line.find("#")


def line_too_long(line: str):
    return len(line) > 79


def indentation_not_multiple(line: str):
    count = 0
    for char in line:
        if char != " ":
            break
        count += 1

    return count % 4 != 0


def unnecessary_semicolon(line: str):
    comment_start = find_comment(line)

    if comment_start != -1:
        statement = line[:comment_start]
    else:
        statement = line

    return statement.rstrip().endswith(";")


def less_spaces_before_comment(line: str):
    comment_start = find_comment(line)

    if comment_start == -1 or comment_start == 0:
        return False

    spaces = 0
    for x in range(comment_start - 1, -1, -1):
        if line[x] == " ":
            spaces += 1
        else:
            break

    return spaces < 2


def todo_found(line: str):
    return re.match("^.*#.*todo", line, re.IGNORECASE)


def find_wrong_blank_lines(lines: list[str]):
    issues = []

    for x in range(3, len(lines)):
        if lines[x - 3] == "" and lines[x - 2] == "" and lines[x - 1] == "" and lines[x] != "":
            issues.append(CodeIssue(x, "S006", "More than two blank lines used before this line"))

    return issues


def blank_spaces_after_def(line: str):
    return re.match(" *\\bdef {2,}\\w", line)


def blank_spaces_after_class(line: str):
    return re.match(" *\\bclass {2,}\\w", line)


def process_file(filepath: str):
    text = read_file(filepath)
    issues = []
    lines = text.split("\n")

    issues.extend(find_wrong_blank_lines(lines))

    tree = ast.parse(text)
    checker = NodeChecker()
    checker.visit(tree)
    issues.extend(checker.issues)

    for x in range(len(lines)):
        line = lines[x]

        if line_too_long(line):
            issues.append(CodeIssue(x, "S001", "Too long"))

        if indentation_not_multiple(line):
            issues.append(CodeIssue(x, "S002", "Indentation is not a multiple of four"))

        if unnecessary_semicolon(line):
            issues.append(CodeIssue(x, "S003", "Unnecessary semicolon"))

        if less_spaces_before_comment(line):
            issues.append(CodeIssue(x, "S004", "At least two spaces required before inline comments"))

        if todo_found(line):
            issues.append(CodeIssue(x, "S005", "TODO found"))

        if blank_spaces_after_class(line):
            issues.append(CodeIssue(x, "S007", "Too many spaces after 'class'"))

        if blank_spaces_after_def(line):
            issues.append(CodeIssue(x, "S007", "Too many spaces after 'def'"))

    return issues


def main():
    files_issues = dict()

    if os.path.isfile(path):
        files_issues[path] = process_file(path)
    elif os.path.isdir(path):
        for filepath in glob.iglob(path + "/**/*.py", recursive=True):
            files_issues[filepath] = process_file(filepath)
    else:
        print("Wrong path")
        exit()

    for filename, issues in files_issues.items():
        issues.sort(key=lambda item: (item.line, item.code))
        for issue in issues:
            print(filename + ": " + str(issue))


if __name__ == '__main__':
    parse_args()
    main()

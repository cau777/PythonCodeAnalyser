# PythonCodeAnalyser

A simple tool that finds common stylistic issues in Python code according to PEP8. It uses Abstract Syntax Tree and
Regular Expressions

## Inspections

* S001 - Line too long (contains more than 79 characters)
* S002 - Indentation is not a multiple of four
* S003 - Unnecessary semicolon after a statement
* S004 - Less than two spaces before inline comments
* S005 - TODO found (in comments only and case-insensitive)
* S006 - More than two blank lines preceding a code line
* S007 - Too many spaces after class/def
* S008 - Class name should be written in CamelCase
* S009 - Function name should be written in snake_case
* S010 - Argument name should be written in snake_case
* S011 - Variable should be written in snake_case (only applies to the ones defined in functions bodies)
* S012 - Default argument value is mutable

## Usage

You should specify the path to a file or directory in the command line. In case a directory is specified, the program
will analyse all python files in the directory and subdirectories.

```
python code_analyzer.py directory-or-file
```

## Examples
```
> python code_analyzer.py /path/to/file/script.py
/path/to/file/script.py: Line 1: S004 At least two spaces required before inline comments
/path/to/file/script.py: Line 2: S003 Unnecessary semicolon
/path/to/file/script.py: Line 3: S001 Too long line
/path/to/file/script.py: Line 3: S003 Unnecessary semicolon
/path/to/file/script.py: Line 6: S001 Too long line
/path/to/file/script.py: Line 11: S006 More than two blank lines used before this line
/path/to/file/script.py: Line 13: S003 Unnecessary semicolon
/path/to/file/script.py: Line 13: S004 At least two spaces required before inline comments
/path/to/file/script.py: Line 13: S005 TODO found
```

```
> python code_analyzer.py /path/to/project
/path/to/project/__init__.py: Line 1: S001 Too long line
/path/to/project/script1.py: Line 1: S004 At least two spaces required before inline comments
/path/to/project/script1.py: Line 2: S003 Unnecessary semicolon
/path/to/project/script2.py: Line 1: S004 At least two spaces required before inline comments
/path/to/project/script2.py: Line 3: S001 Too long line
/path/to/project/somedir/script.py: Line 3: S001 Too long line
/path/to/project/test.py: Line 3: Line 13: S003 Unnecessary semicolon
```

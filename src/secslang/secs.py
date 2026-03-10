from pathlib import Path

from .error import error
from .evaluator.SECSContext import SECSContext
from .parser.parser import parse_tokens
from .scanner.scanner import scan_tokens


def parse_script(src: str, context: SECSContext | None) -> SECSContext:
    error.had_error = False

    tokens = scan_tokens(src)
    if error.had_error:
        return context

    statements = parse_tokens(tokens)
    if error.had_error:
        return context

    if context is None:
        context = SECSContext(statements, None)
    else:
        context.add_statements(statements)

    context.print_all_statements()

    return context

def parse_scripts(srcs: list[str], context: SECSContext | None):
    for src in srcs:
        context = parse_script(src, context)
    return context

def parse_file(path: Path, context: SECSContext | None) -> SECSContext:
    try:
        with open(path, "r") as script_file:
            content = script_file.read()
            return parse_script(content, context)
    except FileNotFoundError:
        print(f"File {path} not found!")
    except IOError:
        print(f"Error reading to file {path}!")

    return context

def parse_files(paths: list[Path], context: SECSContext | None) -> SECSContext:
    for path in paths:
        context = parse_file(path, context)
    return context

def _run_main(script):
    parse_file(script, None)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        _run_main(sys.argv[1])
    else:
        print("usage: src [script]")

from pathlib import Path

from secs.scanner.scanner import scan_tokens


def parse_script(src: str) -> str:
    tokens = scan_tokens(src)
    for token in tokens:
        print(token)

def parse_file(path: Path):
    try:
        with open(path, "r") as script_file:
            content = script_file.read()
            return parse_script(content)
    except FileNotFoundError:
        print(f"File {path} not found!")
    except IOError:
        print(f"Error reading to file {path}!")


def _run_main(script):
    parse_file(script)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        _run_main(sys.argv[1])
    else:
        print("usage: secs [script]")

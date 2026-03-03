from pathlib import Path


def parse_script(file: str) -> str:


def parse_file(path: Path):
    try:
        with open(path, "r") as script_file:
            content = script_file.read()
            return parse_script(content)
    except FileNotFoundError:
        print(f"File {path} not found!")
    except IOError:
        print(f"Error reading to file {path}!")



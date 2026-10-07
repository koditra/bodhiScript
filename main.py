import sys
import os

from interpreter.compiler import compile_source
from interpreter.vm import run


def find_file(filename):
    if not filename.endswith(".bodhi"):
        filename += ".bodhi"

    for root, dirs, files in os.walk("."):
        if filename in files:
            return os.path.join(root, filename)

    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: bodhi <file>")
        sys.exit(1)

    filename = sys.argv[1]
    found_file = find_file(filename)

    if found_file is None:
        print(f"File not found: {filename}")
        sys.exit(1)

    with open(found_file, "r", encoding="utf-8") as file:
        source = file.read()

    try:
        instructions = compile_source(source)
        run(instructions)

    except SyntaxError as error:
        print(f"BodhiScript error: {error}")
        sys.exit(1)

    except RuntimeError as error:
        print(f"Runtime error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
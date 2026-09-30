import sys

KEYWORDS = {
    "maan": "",
    "rakho": "",
    "likha": "print",
    "yadi": "if",
    "agar": "if",
    "anyatha": "else",
    "warna": "else",
    "satya": "True",
    "asatya": "False",
    "shunya": "None",
    "aur": "and",
    "ya": "or",
    "nahi": "not",
    "wapas": "return",
    "karya": "def",
}


def translate(code):
    lines = []

    for line in code.splitlines():
        line = line.strip()

        if not line:
            continue

        for bodhi, python in KEYWORDS.items():
            if line == bodhi:
                line = python
                break

            if line.startswith(bodhi + " "):
                rest = line[len(bodhi):].strip()

                if bodhi in ["maan", "rakho"]:
                    line = rest

                elif bodhi == "likha":
                    line = python + "(" + rest + ")"

                elif bodhi in ["yadi", "agar"]:
                    line = python + " " + rest + ":"

                elif bodhi in ["anyatha", "warna"]:
                    line = python + ":"

                elif bodhi in ["satya", "asatya", "shunya"]:
                    line = python + " " + rest

                elif bodhi in ["aur", "ya", "nahi"]:
                    line = python + " " + rest

                elif bodhi == "wapas":
                    line = python + " " + rest

                elif bodhi == "karya":
                    line = python + " " + rest + ":"

                break

        lines.append(line)

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: bodhi <file>")
        sys.exit(1)

    filename = sys.argv[1]

    if not filename.endswith(".bodhi"):
        filename += ".bodhi"

    with open(filename, "r", encoding="utf-8") as file:
        bodhi = file.read()

    python_code = translate(bodhi)

    exec(python_code)


if __name__ == "__main__":
    main()
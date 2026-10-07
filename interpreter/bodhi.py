import sys
import os
import re

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
    "yavyat": "while",
    "jabtak": "while",
}


def translate_expression(text):
    for bodhi, python in KEYWORDS.items():
        if bodhi in [
            "maan", "rakho", "likha", "yadi", "agar",
            "anyatha", "warna", "wapas", "karya",
            "yavyat", "jabtak"
        ]:
            continue

        text = re.sub(r"\b" + re.escape(bodhi) + r"\b", python, text)

    return text


def translate_statement(line):
    line = line.strip()

    if not line:
        return ""

    if line.startswith("likha("):
        if line.endswith(";"):
            line = line[:-1].strip()

        if not line.endswith(")"):
            raise SyntaxError(f"Invalid likha statement: {line}")

        return "print" + line[5:]

    if not line.endswith(";"):
        raise SyntaxError(
            f"Missing ';' at the end of statement: {line}"
        )

    line = line[:-1].strip()

    if line.startswith("maan "):
        return translate_expression(line[5:].strip())

    if line.startswith("rakho "):
        return translate_expression(line[6:].strip())

    if line.startswith("likha "):
        return "print(" + translate_expression(line[6:].strip()) + ")"

    if line.startswith("wapas "):
        return "return " + translate_expression(line[6:].strip())

    if line == "wapas":
        return "return"

    return translate_expression(line)


def translate_block(line):
    line = line.strip()

    if line.startswith("jabtak "):
        return "while " + translate_expression(line[7:].strip()) + ":"

    if line.startswith("yavyat "):
        return "while " + translate_expression(line[6:].strip()) + ":"

    if line.startswith("karya "):
        return "def " + translate_expression(line[6:].strip()) + ":"

    if line.startswith("yadi "):
        return "if " + translate_expression(line[5:].strip()) + ":"

    if line.startswith("agar "):
        return "if " + translate_expression(line[5:].strip()) + ":"

    if line == "anyatha":
        return "else:"

    if line == "warna":
        return "else:"

    raise SyntaxError(f"Invalid block: {line}")


def translate(code):
    python_lines = []
    indent = 0
    buffer = ""
    parens = 0

    code = code.replace("{", " {\n")
    code = code.replace("}", "\n}\n")

    for raw_line in code.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line == "}":
            if indent == 0:
                raise SyntaxError("Unexpected '}'")

            indent -= 1
            continue

        if line.startswith("} anyatha {"):
            if indent == 0:
                raise SyntaxError("Unexpected 'anyatha'")

            indent -= 1
            python_lines.append("    " * indent + "else:")
            indent += 1
            continue

        if line.startswith("} warna {"):
            if indent == 0:
                raise SyntaxError("Unexpected 'warna'")

            indent -= 1
            python_lines.append("    " * indent + "else:")
            indent += 1
            continue

        if line.endswith("{"):
            block = line[:-1].strip()
            translated = translate_block(block)

            python_lines.append("    " * indent + translated)
            indent += 1
            continue

        if buffer:
            buffer += " " + line
        else:
            buffer = line

        parens += line.count("(") - line.count(")")

        if parens > 0:
            continue

        translated = translate_statement(buffer)
        buffer = ""

        if translated:
            python_lines.append("    " * indent + translated)

    if buffer:
        translated = translate_statement(buffer)

        if translated:
            python_lines.append("    " * indent + translated)

    if indent != 0:
        raise SyntaxError("Missing '}'")

    return "\n".join(python_lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: bodhi <file>")
        sys.exit(1)

    filename = sys.argv[1]

    if not filename.endswith(".bodhi"):
        filename += ".bodhi"

    found_file = None

    for root, dirs, files in os.walk("."):
        if filename in files:
            found_file = os.path.join(root, filename)
            break

    if found_file is None:
        print(f"File not found: {filename}")
        sys.exit(1)

    with open(found_file, "r", encoding="utf-8") as file:
        bodhi = file.read()

    try:
        python_code = translate(bodhi)
        exec(python_code)
    except SyntaxError as e:
        print(f"BodhiScript error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Runtime error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
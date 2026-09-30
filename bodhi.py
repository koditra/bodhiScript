import sys

def translate(code):
    lines = []

    for line in code.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("maan "):
            line = line[5:]

        elif line.startswith("likha "):
            line = "print(" + line[6:] + ")"

        elif line.startswith("yadi "):
            condition = line[5:]
            line = "if " + condition + ":"

        elif line == "anyatha":
            line = "else:"

        lines.append(line)

    return "\n".join(lines)


filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as file:
    bodhi = file.read()

python_code = translate(bodhi)

exec(python_code)
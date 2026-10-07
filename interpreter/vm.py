class VM:
    def __init__(self, instructions):
        self.instructions = instructions
        self.stack = []
        self.variables = {}
        self.ip = 0

    def run(self):
        while self.ip < len(self.instructions):
            instruction = self.instructions[self.ip]
            operation = instruction[0]

            if operation == "PUSH":
                self.stack.append(instruction[1])

            elif operation == "STORE":
                value = self.stack.pop()
                self.variables[instruction[1]] = value

            elif operation == "LOAD":
                name = instruction[1]

                if name not in self.variables:
                    raise RuntimeError(
                        f"Variable '{name}' is not defined."
                    )

                self.stack.append(self.variables[name])

            elif operation == "PRINT":
                value = self.stack.pop()
                print(value)

            elif operation == "ADD":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left + right)

            elif operation == "SUBTRACT":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left - right)

            elif operation == "MULTIPLY":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left * right)

            elif operation == "DIVIDE":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left / right)

            elif operation == "MODULO":
                right = self.stack.pop()
                left = self.stack.pop()
                self.stack.append(left % right)

            elif operation == "HALT":
                return

            else:
                raise RuntimeError(
                    f"Unknown instruction: {operation}"
                )

            self.ip += 1


def run(instructions):
    vm = VM(instructions)
    vm.run()
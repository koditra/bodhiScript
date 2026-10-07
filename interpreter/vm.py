class VM:
    def __init__(self, instructions):
        self.instructions = instructions
        self.stack = []
        self.variables = {}
        self.ip = 0


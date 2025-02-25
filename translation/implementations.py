from block import Block 

class BeginBlock(Block):
    def generate_code(self):
        return "# Початок виконання"

class EndBlock(Block):
    def generate_code(self):
        return "# Кінець виконання"

class AssignmentBlock(Block):
    def __init__(self, block_id, var1, var2=None, value=None):
        super().__init__(block_id)
        self.var1 = var1
        self.var2 = var2
        self.value = value

    def generate_code(self):
        return f"{self.var1} = {self.var2 if self.var2 else self.value}"

class InputBlock(Block):
    def __init__(self, block_id, var):
        super().__init__(block_id)
        self.var = var

    def generate_code(self):
        return f"{self.var} = int(input('Enter value for {self.var}: '))"

class PrintBlock(Block):
    def __init__(self, block_id, var):
        super().__init__(block_id)
        self.var = var

    def generate_code(self):
        return f"print('{self.var} =', {self.var})"

class ConditionBlock(Block):
    def __init__(self, block_id, var, condition, value):
        super().__init__(block_id)
        self.var = var
        self.condition = condition
        self.value = value

    def generate_code(self):
        return f"if {self.var} {self.condition} {self.value}:"
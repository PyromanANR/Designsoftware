from translation.block import Block

class StartBlock(Block):
    def generate_code(self):
        return "# Початок виконання"

class EndBlock(Block):
    def generate_code(self):
        return "# Кінець виконання"

class AssignmentBlock(Block):
    def __init__(self, block_id, var1, var2):
        super().__init__(block_id)
        self.var1 = var1
        self.var2 = var2

    def generate_code(self):
        return f"{self.var1} = {self.var2}"
    
class ConstantBlock(Block):
    def __init__(self, block_id, var, value):
        super().__init__(block_id)
        self.var = var
        self.value = value

    def generate_code(self):
        return f"{self.var} = {self.value}"

class InputBlock(Block):
    def __init__(self, block_id, var):
        super().__init__(block_id)
        self.var = var

    def generate_code(self):
        return f"{self.var} = int(input())"

class PrintBlock(Block):
    def __init__(self, block_id, var):
        super().__init__(block_id)
        self.var = var

    def generate_code(self):
        return f"print('{self.var} =', {self.var})"

class ConditionBlock(Block):
    def __init__(self, block_id, var, condition, value, yes_branch=None, no_branch=None):
        super().__init__(block_id)
        self.var = var
        self.condition = condition
        self.value = value
        self.yes_branch = yes_branch  
        self.no_branch = no_branch 

    def generate_code(self):
        return f"if {self.var} {self.condition} {self.value}:"
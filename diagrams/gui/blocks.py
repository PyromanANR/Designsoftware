from tkinter import simpledialog
from .variable_selector import VariableSelector

# === Базовий клас для блоків ===
class Block:
    def __init__(self, block_id, x, y, shared_variables, parent):
        self.block_id = block_id
        self.x = x
        self.y = y
        self.shared_variables = shared_variables
        self.parent = parent
        self.rect_id = None
        self.text_id = None

    def render(self, canvas):
        pass  # Реалізується в підкласах

# === Класи для кожного типу блоку ===
class AssignmentBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent):
        super().__init__(block_id, x, y, shared_variables, parent)
        selector = VariableSelector(parent, shared_variables)
        self.var1, self.var2 = selector.select_two_variables()

        if not self.var1 or not self.var2:
            raise ValueError("Variable selection was canceled")

    def render(self, canvas):
        self.rect_id = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 50, fill="lightblue", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=f"{self.var1} = {self.var2}", tags=f"block_{self.block_id}")

class ConstantBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent):
        super().__init__(block_id, x, y, shared_variables, parent)
        selector = VariableSelector(parent, shared_variables)

        # Вибір змінної
        self.var = selector.select_variable("Select Variable")
        if not self.var:  # Якщо змінна не була обрана, вийти
            raise ValueError("Variable selection was canceled")

        # Вибір значення
        self.value = simpledialog.askinteger("Input Value", "Enter a constant value:", parent=parent)
        if self.value is None:  # Якщо користувач скасував введення
            raise ValueError("Constant value selection was canceled")

    def render(self, canvas):
        self.rect_id = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 50, fill="lightgreen", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=f"{self.var} = {self.value}", tags=f"block_{self.block_id}")

class InputBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent):
        super().__init__(block_id, x, y, shared_variables, parent)
        selector = VariableSelector(parent, shared_variables)
        self.var = selector.select_variable("Select Variable")

        if not self.var:
            raise ValueError("Variable selection was canceled")

    def render(self, canvas):
        self.rect_id = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 50, fill="yellow", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=f"INPUT {self.var}", tags=f"block_{self.block_id}")

class OutputBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent):
        super().__init__(block_id, x, y, shared_variables, parent)
        selector = VariableSelector(parent, shared_variables)
        self.var = selector.select_variable("Select Variable")

        if not self.var:
            raise ValueError("Variable selection was canceled")

    def render(self, canvas):
        self.rect_id = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 50, fill="orange", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=f"PRINT {self.var}", tags=f"block_{self.block_id}")

class ConditionBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent, condition_type):
        """
        condition_type: "==" або "<"
        """
        super().__init__(block_id, x, y, shared_variables, parent)
        selector = VariableSelector(parent, shared_variables)

        # Вибір змінної
        self.var = selector.select_variable("Select Variable")
        if not self.var:
            raise ValueError("Variable selection was canceled")

        # Вибір значення константи
        self.value = simpledialog.askinteger("Input Value", "Enter a constant value:", parent=parent)
        if self.value is None:
            raise ValueError("Constant value selection was canceled")

        self.condition = condition_type

    def render(self, canvas):
        self.rect_id = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 50, fill="red", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=f"{self.var} {self.condition} {self.value}", tags=f"block_{self.block_id}")
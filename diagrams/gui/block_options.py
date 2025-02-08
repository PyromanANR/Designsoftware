import tkinter as tk
from tkinter import simpledialog

class BlockOptionsDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.selected_option = None
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Select block type:").grid(row=0, column=0, padx=10, pady=10)

        self.var = tk.StringVar(value="Assignment")
        options = ["Assignment (V1 = V2)", "Constant (V = C)", "Input (INPUT V)", "Output (PRINT V)", "Condition (V == C)", "Condition (V < C)"]
        for i, option in enumerate(options):
            tk.Radiobutton(master, text=option, variable=self.var, value=option).grid(row=i + 1, column=0, sticky="w", padx=20)

    def apply(self):
        self.selected_option = self.var.get()

# === Базовий клас для блоків ===
class Block:
    def __init__(self, block_id, x, y):
        self.block_id = block_id
        self.x = x
        self.y = y
        self.rect_id = None
        self.text_id = None

    def render(self, canvas):
        pass  # Реалізується в підкласах

# === Класи для кожного типу блоку ===
class AssignmentBlock(Block):
    def __init__(self, block_id, x, y, var1, var2):
        super().__init__(block_id, x, y)
        self.var1 = var1
        self.var2 = var2

    def render(self, canvas):
        self.rect_id = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 50, fill="lightblue", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=f"{self.var1} = {self.var2}", tags=f"block_{self.block_id}")

class ConstantBlock(Block):
    def __init__(self, block_id, x, y, var, value):
        super().__init__(block_id, x, y)
        self.var = var
        self.value = value

    def render(self, canvas):
        self.rect_id = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 50, fill="lightgreen", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=f"{self.var} = {self.value}", tags=f"block_{self.block_id}")

class InputBlock(Block):
    def __init__(self, block_id, x, y, var):
        super().__init__(block_id, x, y)
        self.var = var

    def render(self, canvas):
        self.rect_id = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 50, fill="yellow", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=f"INPUT {self.var}", tags=f"block_{self.block_id}")

class OutputBlock(Block):
    def __init__(self, block_id, x, y, var):
        super().__init__(block_id, x, y)
        self.var = var

    def render(self, canvas):
        self.rect_id = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 50, fill="orange", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=f"PRINT {self.var}", tags=f"block_{self.block_id}")

class ConditionBlock(Block):
    def __init__(self, block_id, x, y, var, value, condition):
        super().__init__(block_id, x, y)
        self.var = var
        self.value = value
        self.condition = condition

    def render(self, canvas):
        self.rect_id = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 50, fill="red", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=f"{self.var} {self.condition} {self.value}", tags=f"block_{self.block_id}")

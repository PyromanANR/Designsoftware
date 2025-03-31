import customtkinter as ctk
from tkinter import messagebox
from ..variable_selector import VariableSelector
from ..block import Block

class ConstantBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent):
        super().__init__(block_id, x, y, shared_variables, parent)
        selector = VariableSelector(parent, shared_variables)

        # Вибір змінної
        self.var = selector.select_variable("Виберіть змінну")
        if not self.var:
            raise ValueError("Вибір змінної скасовано")

        # Введення значення через CTkInputDialog
        dialog = ctk.CTkInputDialog(text=f"Введіть константне значення для {self.var}:", title="Константа")
        value_str = dialog.get_input()
        if value_str is None:
            raise ValueError("Скасовано введення константи")

        try:
            self.value = int(value_str)
            if not (0 <= self.value <= 2**31 - 1):
                raise ValueError
        except ValueError:
            messagebox.showerror("Помилка", "Константа має бути цілим числом у межах 0…2³¹-1.")
            raise ValueError("Некоректне значення")

        self.text = f"{self.var} = {self.value}"

    def render(self, canvas):
        self.shape_id = canvas.create_rectangle(
            self.x, self.y, self.x + 200, self.y + 50,
            fill="white", tags=f"block_{self.block_id}"
        )
        self.text_id = canvas.create_text(
            self.x + 100, self.y + 25, text=self.text, tags=f"block_{self.block_id}"
        )

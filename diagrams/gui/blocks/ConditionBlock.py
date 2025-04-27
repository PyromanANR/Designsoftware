import customtkinter as ctk
from tkinter import messagebox
from ..variable_selector import VariableSelector
from ..block import Block

class ConditionBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent, condition_type):
        """
        condition_type: "==" або "<"
        """
        super().__init__(block_id, x, y, shared_variables, parent)
        selector = VariableSelector(parent, shared_variables)

        self.var = selector.select_variable("Виберіть змінну")
        if not self.var:
            raise ValueError("Вибір змінної скасовано")

        dialog = ctk.CTkInputDialog(
            text=f"Введіть значення для перевірки ({self.var} {condition_type} ...):",
            title="Константа умови"
        )
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

        self.condition = condition_type
        self.text = f"{self.var} {self.condition} {self.value}"

    def render(self, canvas):
        width = 280
        height = 80

        points = (
            self.x + width / 2, self.y,                 # Верхній центр
            self.x + width, self.y + height / 2,        # Правий центр
            self.x + width / 2, self.y + height,        # Нижній центр
            self.x, self.y + height / 2                 # Лівий центр
        )
        self.shape_id = canvas.create_polygon(
            points,
            fill="white",
            outline="black",
            width=2,
            tags=f"block_{self.block_id}"
        )
        self.text_id = canvas.create_text(
            self.x + width / 2, self.y + height / 2,
            text=self.text,
            font=("Segoe UI", 20, "bold"),
            fill="black",
            tags=f"block_{self.block_id}"
        )

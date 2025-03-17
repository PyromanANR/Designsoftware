from tkinter import simpledialog
from ..variable_selector import VariableSelector
from ..block import Block

class ConstantBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent):
        super().__init__(block_id, x, y, shared_variables, parent)
        selector = VariableSelector(parent, shared_variables)

        # Вибір змінної
        self.var = selector.select_variable("Виберіть змінну")
        if not self.var:  # Якщо змінна не була обрана, вийти
            raise ValueError("Вибір змінної скасовано")

        # Вибір значення
        self.value = simpledialog.askinteger("Вхідне значення", "Введіть константне значення:", parent=parent)
        if self.value is None:  # Якщо користувач скасував введення
            raise ValueError("Скасовано введення константи")

        self.text = f"{self.var} = {self.value}"

    def render(self, canvas):
        self.shape_id = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 50, fill="white", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=self.text, tags=f"block_{self.block_id}")

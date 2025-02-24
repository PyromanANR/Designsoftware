from tkinter import simpledialog
from ..variable_selector import VariableSelector
from ..block import Block

class ConditionBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent, condition_type):
        """
        condition_type: "==" або "<"
        """
        super().__init__(block_id, x, y, shared_variables, parent)
        selector = VariableSelector(parent, shared_variables)

        # Вибір змінної
        self.var = selector.select_variable("Виберіть змінну")
        if not self.var:
            raise ValueError("Вибір змінної скасовано")

        # Вибір значення константи
        self.value = simpledialog.askinteger("Вхідне значення", "Введіть константне значення:", parent=parent)
        if self.value is None:
            raise ValueError("Скасовано введення константи")

        self.condition = condition_type

    def render(self, canvas):
        width, height = 200, 50
        # Координати ромба: верх, правий, низ, лівий
        points = (
            self.x + width / 2, self.y,  # Верхній центр
            self.x + width, self.y + height / 2,  # Правий центр
            self.x + width / 2, self.y + height,  # Нижній центр
            self.x, self.y + height / 2  # Лівий центр
        )
        self.shape_id = canvas.create_polygon(
            points,
            fill="white", outline="black",
            tags=f"block_{self.block_id}"
        )
        self.text_id = canvas.create_text(
            self.x + width / 2, self.y + height / 2,
            text=f"{self.var} {self.condition} {self.value}",
            tags=f"block_{self.block_id}"
        )
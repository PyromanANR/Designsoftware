from ..variable_selector import VariableSelector
from ..block import Block

class OutputBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent):
        super().__init__(block_id, x, y, shared_variables, parent)
        selector = VariableSelector(parent, shared_variables)
        self.var = selector.select_variable("Виберіть змінну")

        if not self.var:
            raise ValueError("Вибір змінної скасовано")

    def render(self, canvas):
        offset, width, height = 20, 200, 50
        self.shape_id = canvas.create_polygon(
            self.x + offset, self.y,  # Верхня ліва
            self.x + offset + width, self.y,  # Верхня права
            self.x + width, self.y + height,  # Нижня права
            self.x, self.y + height,  # Нижня ліва
            fill="white", outline="black",
            tags=f"block_{self.block_id}"
        )
        self.text_id = canvas.create_text(
            self.x + offset / 2 + width / 2, self.y + height / 2,
            text=f"PRINT {self.var}",
            tags=f"block_{self.block_id}"
        )
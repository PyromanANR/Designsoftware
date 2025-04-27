from ..variable_selector import VariableSelector
from ..block import Block

class AssignmentBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent):
        super().__init__(block_id, x, y, shared_variables, parent)
        selector = VariableSelector(parent, shared_variables)
        self.var1, self.var2 = selector.select_two_variables()

        if not self.var1 or not self.var2:
            raise ValueError("Вибір змінної скасовано")

        self.text = f"{self.var1} = {self.var2}"

    def render(self, canvas):
        width = 280
        height = 80

        self.shape_id = canvas.create_rectangle(
            self.x, self.y, self.x + width, self.y + height,
            fill="white",
            outline="black",
            width=2,
            tags=f"block_{self.block_id}"
        )
        self.text_id = canvas.create_text(
            self.x + width // 2, self.y + height // 2,
            text=self.text,
            font=("Segoe UI", 20, "bold"),
            fill="black",
            tags=f"block_{self.block_id}"
        )

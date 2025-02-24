from ..variable_selector import VariableSelector
from ..block import Block

class AssignmentBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent):
        super().__init__(block_id, x, y, shared_variables, parent)
        selector = VariableSelector(parent, shared_variables)
        self.var1, self.var2 = selector.select_two_variables()

        if not self.var1 or not self.var2:
            raise ValueError("Вибір змінної скасовано")

    def render(self, canvas):
        self.shape_id = canvas.create_rectangle(self.x, self.y, self.x + 200, self.y + 50, fill="white", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=f"{self.var1} = {self.var2}", tags=f"block_{self.block_id}")

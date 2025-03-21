from ..block import Block

class StartBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent):
        super().__init__(block_id, x, y, shared_variables, parent)
        self.text = "Початок"

    def render(self, canvas):
        self.shape_id = canvas.create_oval(self.x, self.y, self.x + 200, self.y + 50, fill="white", tags=f"block_{self.block_id}")
        self.text_id = canvas.create_text(self.x + 100, self.y + 25, text=self.text, tags=f"block_{self.block_id}")
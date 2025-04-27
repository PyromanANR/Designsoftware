from ..block import Block

class EndBlock(Block):
    def __init__(self, block_id, x, y, shared_variables, parent):
        super().__init__(block_id, x, y, shared_variables, parent)
        self.text = "Кінець"

    def render(self, canvas):
        width = 280
        height = 80

        self.shape_id = canvas.create_oval(
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

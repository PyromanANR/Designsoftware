class Diagram:
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    def render(self, canvas):
        canvas.delete("all")
        for block in self.blocks:
            block.render(canvas)
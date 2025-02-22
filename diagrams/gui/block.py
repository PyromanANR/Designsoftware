# === Базовий клас для блоків ===
class Block:
    def __init__(self, block_id, x, y, shared_variables, parent):
        self.block_id = block_id
        self.x = x
        self.y = y
        self.shared_variables = shared_variables
        self.parent = parent
        self.shape_id = None
        self.text_id = None

    def render(self, canvas):
        pass  # Реалізується в підкласах
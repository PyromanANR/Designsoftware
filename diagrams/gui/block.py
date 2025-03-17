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
        self.next_blocks = []  # Наступні блоки
        self.text = ""

    def render(self, canvas):
        pass  # Реалізується в підкласах

    def add_next_block(self, block, condition=None):
        """Додає наступний блок (для умовного блоку додається мітка 'так'/'ні')."""
        if condition:
            self.next_blocks.append((block, condition))
        else:
            self.next_blocks.append(block)
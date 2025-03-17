from .blocks.ConditionBlock import ConditionBlock
class Diagram:
    def __init__(self, name, shared_variables):
        self.blocks = []
        self.name = name
        self.shared_variables = shared_variables

    def add_block(self, block):
        self.blocks.append(block)

    def render(self, canvas):
        # Видаляємо тільки блоки (але не зв’язки та інші елементи)
        for block in self.blocks:
            canvas.delete(f"block_{block.block_id}")

            # Малюємо блоки заново
        for block in self.blocks:
            block.render(canvas)

    def to_dict(self):
        """Повертає JSON-структуру діаграми з блоками та спільними змінними."""
        data = {
            "name": self.name,
            "blocks": [],
            "shared_variables": self.shared_variables.get_variables() if self.shared_variables else {}
        }

        for block in self.blocks:
            block_data = {
                "id": block.block_id,
                "type": block.__class__.__name__,
                "x": block.x,
                "y": block.y,
                "text": block.text,
                "connections": []
            }

            if isinstance(block, ConditionBlock):
                for next_block, condition in block.next_blocks:
                    block_data["connections"].append({
                        "to": next_block.block_id,
                        "condition": condition
                    })
            else:
                for next_block in block.next_blocks:
                    block_data["connections"].append({"to": next_block.block_id})

            data["blocks"].append(block_data)

        return data
import tkinter as tk
from .blocks.ConditionBlock import ConditionBlock
from .blocks.AssignmentBlock import AssignmentBlock
from .blocks.ConstantBlock import ConstantBlock
from .blocks.InputBlock import InputBlock
from .blocks.OutputBlock import OutputBlock
from .blocks.EndBlock import EndBlock
from .blocks.StartBlock import StartBlock

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

    def load_from_dict(self, data, parent_canvas):
        block_map = {}
        self.blocks.clear()

        # Додаємо змінні у спільну пам'ять
        for var_name, value in data.get("shared_variables", {}).items():
            self.shared_variables.add_variable(var_name, value)

        for block_data in data["blocks"]:
            block_class = globals().get(block_data["type"], None)
            if block_class:
                if block_data["type"] == "ConditionBlock":
                    # Уникаємо виклику __init__, щоб не з'являлися спливаючі вікна
                    block = block_class.__new__(block_class)
                    block.block_id = block_data["id"]
                    block.x = block_data["x"]
                    block.y = block_data["y"]
                    block.shared_variables = self.shared_variables
                    block.parent = parent_canvas
                    block.text = block_data["text"]
                    block.next_blocks = []
                    block.condition_type = block_data.get("condition_type", "==")  # Призначаємо тип умови вручну
                else:
                    # Для всіх інших блоків створюємо через __new__, щоб уникнути виклику VariableSelector
                    block = block_class.__new__(block_class)
                    block.block_id = block_data["id"]
                    block.x = block_data["x"]
                    block.y = block_data["y"]
                    block.shared_variables = self.shared_variables
                    block.parent = parent_canvas
                    block.text = block_data["text"]
                    block.next_blocks = []

                    # Запобігаємо виклику VariableSelector у __init__, якщо це передбачено в конкретному класі
                    if hasattr(block, "var1") and hasattr(block, "var2"):
                        block.var1 = block_data.get("var1", None)
                        block.var2 = block_data.get("var2", None)
                    elif hasattr(block, "variable"):
                        block.variable = block_data.get("variable", None)
                    elif hasattr(block, "constant_value"):
                        block.constant_value = block_data.get("constant_value", None)

                self.add_block(block)
                block_map[block.block_id] = block

        # Викликаємо render() для всіх блоків, щоб вони отримали shape_id
        for block in self.blocks:
            block.render(parent_canvas)

        # Відновлюємо зв’язки між блоками
        for block_data in data["blocks"]:
            block = block_map[block_data["id"]]
            for connection in block_data["connections"]:
                target_block = block_map.get(connection["to"], None)
                if target_block:
                    condition = connection.get("condition", None)
                    block.add_next_block(target_block, condition)

        # Виклик методу redraw_connections з DiagramEditor
        parent_canvas.redraw_connections()
from implementations import AssignmentBlock, InputBlock, PrintBlock, ConditionBlock, BeginBlock, EndBlock

class BlockFactory:
    """Фабрика для створення блоків"""

    @staticmethod
    def create_block(block_data):
        block_type = block_data["type"]
        if block_type == "begin":
            return BeginBlock(block_data["id"])
        elif block_type == "end":
            return EndBlock(block_data["id"])
        elif block_type == "assignment":
            return AssignmentBlock(block_data["id"], block_data["var1"], block_data.get("var2"), block_data.get("value"))
        elif block_type == "input":
            return InputBlock(block_data["id"], block_data["var"])
        elif block_type == "print":
            return PrintBlock(block_data["id"], block_data["var"])
        elif block_type == "condition":
            return ConditionBlock(block_data["id"], block_data["var"], block_data["condition"], block_data["value"])
        else:
            raise ValueError(f"Unknown block type: {block_type}")
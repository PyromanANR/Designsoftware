from implementations import StartBlock, EndBlock, AssignmentBlock, ConstantBlock, InputBlock, PrintBlock, ConditionBlock

class BlockFactory:
    """Фабрика для створення блоків"""

    @staticmethod
    def create_block(block_data):
        block_type = block_data["type"]
        if block_type == "StartBlock":
            return StartBlock(block_data["id"])
        elif block_type == "EndBlock":
            return EndBlock(block_data["id"])
        elif block_type == "AssignmentBlock":
            return AssignmentBlock(block_data["id"], block_data["text"].split("=")[0].strip(), block_data["text"].split("=")[1].strip())
        elif block_type == "ConstantBlock":
            return ConstantBlock(block_data["id"], block_data["text"].split("=")[0].strip(), int(block_data["text"].split("=")[1].strip()))
        elif block_type == "InputBlock":
            return InputBlock(block_data["id"], block_data["text"].replace("INPUT", "").strip())
        elif block_type == "PrintBlock":
            return PrintBlock(block_data["id"], block_data["text"].replace("PRINT", "").strip())
        elif block_type == "ConditionBlock":
            parts = block_data["text"].split(" ")
            return ConditionBlock(block_data["id"], parts[0].strip(), parts[1].strip(), parts[2].strip())
        else:
            raise ValueError(f"Unknown block type: {block_type}")
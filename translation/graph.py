from factory import BlockFactory
from implementations import StartBlock, ConditionBlock

from factory import BlockFactory
from implementations import StartBlock, ConditionBlock

class Graph:
    """Граф для представлення потоку виконання блок-схеми."""

    def __init__(self):
        self.blocks = {}  # Всі блоки
        self.connections = {}  # З'єднання між блоками

    def build_from_json(self, thread_data):
        """Створює граф з JSON-даних потоку."""
        for block_data in thread_data["blocks"]:
            block = BlockFactory.create_block(block_data)
            self.add_block(block)

        for block_data in thread_data["blocks"]:
            block_id = block_data["id"]
            for connection in block_data.get("connections", []):
                to_id = connection["to"]
                condition = connection.get("condition")
                self.add_connection(block_id, to_id, condition)

                block = self.blocks.get(block_id)
                if isinstance(block, ConditionBlock):
                    if condition == "так":
                        block.yes_branch = to_id
                    elif condition == "ні":
                        block.no_branch = to_id

    def add_block(self, block):
        """Додає блок у граф."""
        self.blocks[block.block_id] = block
        self.connections[block.block_id] = []

    def add_connection(self, from_id, to_id, condition=None):
        """Додає з'єднання між блоками."""
        if from_id not in self.blocks or to_id not in self.blocks:
            raise ValueError(f"Помилка: Блок {from_id} або {to_id} не існує!")
        self.connections[from_id].append((to_id, condition))

    def detect_loops(self):
        """Визначає циклічні послідовності в графі."""
        visited = set()
        stack = set()
        loops = set()

        def dfs(node):
            if node in stack:
                loops.add(node)
                return
            if node in visited:
                return
            visited.add(node)
            stack.add(node)
            for neighbor, _ in self.connections.get(node, []):
                dfs(neighbor)
            stack.remove(node)

        for block_id in self.blocks:
            if block_id not in visited:
                dfs(block_id)
        return loops

    def generate_code(self):
        """Генерує Python-код у послідовному порядку з підтримкою циклів."""
        code_lines = []
        queue = []
        processed = set()
        loops = self.detect_loops()

        start_block = next((b for b in self.blocks.values() if isinstance(b, StartBlock)), None)
        if start_block:
            queue.append(start_block.block_id)

        after_condition_blocks = set()
        inside_loop = False
        indent_level = 0

        while queue:
            block_id = queue.pop(0)
            if block_id in processed:
                continue
            processed.add(block_id)

            block = self.blocks[block_id]
            next_blocks = self.connections.get(block_id, [])

            if block_id in loops and not inside_loop:
                code_lines.append("while True:")
                inside_loop = True
                indent_level = 1  # Start indentation for looped blocks

            indent = "    " * indent_level  # Apply proper indentation

            if isinstance(block, ConditionBlock):
                condition = f"{block.var} {block.condition} {block.value}"
                yes_block = block.yes_branch
                no_block = block.no_branch

                code_lines.append(f"{indent}if {condition}:")
                if yes_block:
                    code_lines.append(f"{indent}    {self.blocks[yes_block].generate_code()}")
                    queue.append(yes_block)
                    after_condition_blocks.add(yes_block)
                
                code_lines.append(f"{indent}else:")
                if no_block:
                    code_lines.append(f"{indent}    {self.blocks[no_block].generate_code()}")
                    queue.append(no_block)
                    after_condition_blocks.add(no_block)
                
                common_next = set()
                if yes_block and no_block:
                    yes_next = {b[0] for b in self.connections.get(yes_block, [])}
                    no_next = {b[0] for b in self.connections.get(no_block, [])}
                    common_next = yes_next.intersection(no_next)
                
                for next_block in common_next:
                    queue.append(next_block)
            else:
                if block_id not in after_condition_blocks:
                    code_lines.append(f"{indent}{block.generate_code()}")
                for next_block, _ in next_blocks:
                    queue.append(next_block)

            # If we exit the loop, reset indentation
            if block_id in loops and inside_loop:
                inside_loop = False
                indent_level = 0  # Reset indentation after loop

        return "\n".join(code_lines)

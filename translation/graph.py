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
        """Генерує Python-код у послідовному порядку з підтримкою циклів та унікальних блоків після if."""
        code_lines = []
        queue = []
        processed = set()
        loops = self.detect_loops()

        start_block = next((b for b in self.blocks.values() if isinstance(b, StartBlock)), None)
        if start_block:
            queue.append(start_block.block_id)

        inside_loop = False
        indent_level = 0
        loop_blocks = set()
        unique_blocks_after_if = set()

        # Identify all blocks that are part of a loop
        for block_id in loops:
            loop_blocks.add(block_id)
            for next_block, _ in self.connections.get(block_id, []):
                loop_blocks.add(next_block)

        while queue:
            block_id = queue.pop(0)
            if block_id in processed:
                continue
            processed.add(block_id)

            block = self.blocks[block_id]
            next_blocks = self.connections.get(block_id, [])

            # If entering a loop, add 'while True:' and increase indentation
            if block_id in loops and not inside_loop:
                code_lines.append("while True:")
                inside_loop = True
                indent_level += 1

            indent = "    " * indent_level  # Apply correct indentation

            # Handle conditional blocks
            if isinstance(block, ConditionBlock):
                condition = f"{block.var} {block.condition} {block.value}"
                yes_block = block.yes_branch
                no_block = block.no_branch

                # IF condition
                code_lines.append(f"{indent}if {condition}:")
                indent_level += 1  # Increase indentation inside IF block

                if yes_block:
                    queue.append(yes_block)
                    code_lines.append(f"{'    ' * indent_level}{self.blocks[yes_block].generate_code()}")
                    unique_blocks_after_if.add(yes_block)  # Mark for unique execution

                indent_level -= 1  # Reset after IF

                # ELSE condition (if exists)
                if no_block:
                    code_lines.append(f"{indent}else:")
                    indent_level += 1  # Increase indentation inside ELSE block
                    queue.append(no_block)
                    code_lines.append(f"{'    ' * indent_level}{self.blocks[no_block].generate_code()}")
                    unique_blocks_after_if.add(no_block)  # Mark for unique execution
                    indent_level -= 1  # Reset after ELSE

                # Find blocks that come **after both IF and ELSE** (common blocks)
                common_next = set()
                if yes_block and no_block:
                    yes_next = {b[0] for b in self.connections.get(yes_block, [])}
                    no_next = {b[0] for b in self.connections.get(no_block, [])}
                    common_next = yes_next.intersection(no_next)

                # Ensure common blocks only appear **once** after IF-ELSE
                for next_block in common_next:
                    if next_block not in unique_blocks_after_if:
                        queue.append(next_block)

            else:
                # Generate normal block code
                if block_id not in unique_blocks_after_if:
                    code_lines.append(f"{indent}{block.generate_code()}")

                # Add next blocks to the queue
                for next_block, _ in next_blocks:
                    queue.append(next_block)

            # If exiting the loop, reset indentation
            if block_id in loops and all(nb not in loop_blocks for nb, _ in next_blocks):
                inside_loop = False
                indent_level -= 1

        return "\n".join(code_lines)

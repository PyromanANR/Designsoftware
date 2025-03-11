from factory import BlockFactory
from implementations import StartBlock, ConditionBlock

class Graph:
    """Граф для представлення потоку виконання блок-схеми."""

    def __init__(self):
        self.blocks = {}  # Всі блоки
        self.connections = {}  # З'єднання між блоками

    def build_from_json(self, thread_data):
        """Створює граф з JSON-даних потоку."""
        # Додаємо блоки
        for block_data in thread_data["blocks"]:
            block = BlockFactory.create_block(block_data)
            self.add_block(block)

        # Додаємо з'єднання
        for block_data in thread_data["blocks"]:
            block_id = block_data["id"]
            for connection in block_data.get("connections", []):
                to_id = connection["to"]
                condition = connection.get("condition")  # Умова (якщо є)
                self.add_connection(block_id, to_id, condition)

                # Оновлення умов для ConditionBlock
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

    def generate_code(self):
        """Генерує Python-код з урахуванням умов і циклів."""
        code_lines = []
        visited = set()

        def dfs(block_id, indent_level=0):
            """Обхід графа в глибину для генерації коду."""
            if block_id in visited:
                return
            visited.add(block_id)

            block = self.blocks[block_id]
            indentation = "    " * indent_level
            next_blocks = self.connections.get(block_id, [])

            if isinstance(block, ConditionBlock):
                condition = f"{block.var} {block.condition} {block.value}"
                yes_block = block.yes_branch
                no_block = block.no_branch

                # Вставляємо умову
                code_lines.append(f"{indentation}if {condition}:")
                if yes_block:
                    dfs(yes_block, indent_level + 1)

                if no_block:
                    code_lines.append(f"{indentation}else:")
                    dfs(no_block, indent_level + 1)

                # Handle blocks that come after both branches
                yes_next = {b[0] for b in self.connections.get(yes_block, [])}
                no_next = {b[0] for b in self.connections.get(no_block, [])}
                common_blocks = yes_next.intersection(no_next)

                for block in common_blocks:
                    if block not in visited:
                        dfs(block, indent_level)

            else:
                # Виконання звичайних блоків
                code_lines.append(f"{indentation}{block.generate_code()}")

                # Виконання наступного блоку
                for next_block, _ in next_blocks:
                    dfs(next_block, indent_level)

        # Починаємо з блоку початку
        start_block = next((b for b in self.blocks.values() if isinstance(b, StartBlock)), None)
        if start_block:
            dfs(start_block.block_id)

        return "\n".join(code_lines)

import json
  
class Block:
    def __init__(self, block_id, block_type, x=None, y=None, **kwargs):
        """
        Конструктор блоку.

        :param block_id: ID блоку
        :param block_type: Тип блоку (assignment, input, condition)
        :param x: X-координата (необов'язкова)
        :param y: Y-координата (необов'язкова)
        :param kwargs: Додаткові параметри (наприклад, змінні, умови)
        """
        self.block_id = block_id
        self.block_type = block_type
        self.x = x
        self.y = y
        self.extra_attributes = kwargs  # Додаткові параметри блоку

    def __repr__(self):
        return f"Block(id={self.block_id}, type={self.block_type}, x={self.x}, y={self.y}, attrs={self.extra_attributes})"


class Thread:
    def __init__(self, thread_id, blocks, connections):
        """
        Конструктор потоку виконання.

        :param thread_id: ID потоку
        :param blocks: Список блоків у потоці
        :param connections: Зв'язки між блоками
        """
        self.thread_id = thread_id
        self.blocks = {}  # Зберігаємо блоки у вигляді словника (ID -> Block)
        self.graph = {}  # Граф (ID -> список наступних блоків)

        # Створюємо блоки
        for block in blocks:
            block_id = block["id"]
            if block_id in self.blocks:
                raise ValueError(f"Помилка: ID блоку {block_id} не унікальний!")

            self.blocks[block_id] = Block(
                block_id=block_id,
                block_type=block["type"],
                x=block.get("x"),
                y=block.get("y"),
                **{k: v for k, v in block.items() if k not in ["id", "type", "x", "y"]}  # Видаляємо зайві аргументи
            )

            # Ініціалізуємо граф (порожній список суміжності)
            self.graph[block_id] = []

        # Перевіряємо коректність з'єднань і будуємо граф
        for conn in connections:
            from_id, to_id = conn["from"], conn["to"]
            if from_id not in self.blocks or to_id not in self.blocks:
                raise ValueError(f"Помилка: некоректне з'єднання {from_id} → {to_id}, ID не існує!")

            self.graph[from_id].append(to_id)  # Додаємо зв'язок у граф

    def __repr__(self):
        return f"Thread(id={self.thread_id}, blocks={list(self.blocks.keys())}, graph={self.graph})"


def load_json(file_path):
    """
    Завантажує JSON і парсить потоки та блоки.

    :param file_path: Шлях до JSON-файлу
    :return: (спільні змінні, список потоків)
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Перевірка, чи містить JSON необхідні поля
    if "shared_variables" not in data or "threads" not in data:
        raise ValueError("Помилка: JSON не містить необхідних ключів 'shared_variables' або 'threads'!")

    shared_variables = data["shared_variables"]
    threads = [Thread(thread_data["id"], thread_data["blocks"], thread_data["connections"])
               for thread_data in data["threads"]]

    return shared_variables, threads


# === Виконання ===
if __name__ == "__main__":
    file_path = "example.json"
    try:
        shared_vars, threads = load_json(file_path)
        print("Спільні змінні:", shared_vars)
        for thread in threads:
            print(thread)  # Вивід інформації про потік
            for block in thread.blocks.values():
                print("  ", block)  # Вивід інформації про блоки
    except Exception as e:
        print(f"Помилка: {e}")

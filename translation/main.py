import json
import os
from thread import Thread
from code_writer import Writer

# Директорія, в якій зберігаються JSON-файли
json_dir = os.path.join(os.path.dirname(__file__), "diagramJson")

# Отримуємо список усіх JSON-файлів у цій директорії
json_files = [os.path.join(json_dir, file) for file in os.listdir(json_dir) if file.endswith(".json")]

# Загальні змінні
shared_variables = {}

# Список потоків
threads = []

# Читаємо JSON файли та створюємо потоки
for filename in json_files:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Оновлюємо спільні змінні
        shared_variables.update(data.get("shared_variables", {}))

        # Створюємо потік
        thread = Thread(thread_id=data["name"], shared_vars=shared_variables)
        thread.build_from_json(data)
        threads.append(thread)

    except Exception as e:
        print(f"Помилка при обробці файлу {filename}: {e}")

# Записуємо всі потоки у файл
writer = Writer("generated_code.py")
writer.write_code(threads, shared_variables)

print("Код згенеровано у файлі 'generated_code.py'")

if __name__ == "__main__":
    print("Скрипт виконано успішно!")

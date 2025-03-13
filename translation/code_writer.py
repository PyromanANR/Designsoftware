import os
import threading

class Writer:
    """Клас для запису згенерованого коду в файл та запуску потоків."""

    def __init__(self, filename):
        self.directory = os.path.join(os.path.dirname(__file__), "codePython")
        os.makedirs(self.directory, exist_ok=True)  
        self.filepath = os.path.join(self.directory, filename)

    def write_code(self, threads, shared_vars):
        """Записує згенерований код усіх потоків у файл та забезпечує їх паралельне виконання."""
        with open(self.filepath, "w", encoding="utf-8") as file:
            file.write("# Автоматично згенерований код\n\n")
            
            # Записуємо спільні змінні
            file.write("# Спільні змінні\n")
            for var, value in shared_vars.items():
                file.write(f"{var} = {value}\n")
            file.write("\n")

            # Записуємо функції для потоків
            for thread in threads:
                file.write(f"def thread_{thread.thread_id}():\n")
                thread_code = thread.get_code().split("\n")
                for line in thread_code:
                    file.write(f"    {line}\n")
                file.write("\n")

            # Запуск потоків
            file.write("if __name__ == \"__main__\":\n")
            file.write("    import threading\n")
            for thread in threads:
                file.write(f"    t_{thread.thread_id} = threading.Thread(target=thread_{thread.thread_id})\n")
                file.write(f"    t_{thread.thread_id}.start()\n")
            file.write("\n")

            # Додатково: Чекаємо завершення потоків (якщо необхідно)
            file.write("    for t in threading.enumerate():\n")
            file.write("        if t is not threading.current_thread():\n")
            file.write("            t.join()\n")


import io
import sys
import builtins

class CodeRunner:
    """
    Відповідає за запуск коду (Python) з файлу та повернення stdout.
    Використовує exec() із захопленням stdout та підміною sys.stdin.
    """

    def run_file(self, file_path: str, input_data: str = "") -> str:
        """Зчитує код із файлу, виконує його з підстановкою вхідних даних та повертає stdout."""
        with open(file_path, "r", encoding="utf-8") as f:
            code_text = f.read()

        backup_stdout = sys.stdout
        backup_stdin = sys.stdin
        backup_input = builtins.input  # зберігаємо оригінальну input
        output_buffer = io.StringIO()
        input_buffer = io.StringIO(input_data)

        sys.stdout = output_buffer
        sys.stdin = input_buffer

        # Перепризначаємо built-in input, щоб використовувати наш input_buffer
        builtins.input = lambda prompt="": input_buffer.readline().rstrip("\n")

        try:
            local_env = {}
            exec(code_text, {}, local_env)
        finally:
            sys.stdout = backup_stdout
            sys.stdin = backup_stdin
            builtins.input = backup_input  # відновлюємо оригінальну input

        return output_buffer.getvalue()


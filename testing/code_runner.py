import io
import sys

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
        output_buffer = io.StringIO()
        input_buffer = io.StringIO(input_data)

        sys.stdout = output_buffer
        sys.stdin = input_buffer

        try:
            local_env = {}
            exec(code_text, {}, local_env)
        finally:
            sys.stdout = backup_stdout
            sys.stdin = backup_stdin

        return output_buffer.getvalue()

import io
import sys
import threading
import time

class Tester:
    """
    Клас для запуску тестів, обробки недетермінованості, раннього виходу тощо.
    У спрощеному вигляді просто виконує код із заданими input-даними,
    порівнює вивід із expected_output.
    Для недетермінованості потрібно перебирати інтерлівінги потоків.
    """

    def run_tests(self, code_path: str, tests: list, k: int = 20):
        """
        Запускає тести на code_path із урахуванням обмеження K (до 20).
        Повертає:
          - test_results: список словників із полями {"status": "OK"/"FAIL"/"ERROR", ...}
          - coverage_percent: відсоток "пройдених" виконань з <= K кроками (у спрощеній версії - фіктивно).
        """
        test_results = []
        # Для прикладу зберігатимемо "скільки виконань ми перевірили" у visited_count
        visited_count = 0
        total_possible = 1  # У реальному випадку: кількість усіх інтерлівінгів <= K

        for test_case in tests:
            # Імітуємо "багатократний запуск" — у спрощеному вигляді робимо один запуск
            # Можна було б перебирати декілька інтерлівінгів...

            result = self._execute_code_with_input(code_path, test_case.get("input", ""))
            expected = test_case.get("expected_output", "")

            if result.strip() == expected.strip():
                test_results.append({"status": "OK", "actual": result})
            else:
                test_results.append({"status": f"FAIL (expected '{expected}', got '{result}')", "actual": result})

            visited_count += 1

        # Обчислюємо відсоток покриття (у реальному сценарії - складніший)
        coverage_percent = (visited_count / (total_possible or 1)) * 100

        return test_results, coverage_percent

    def _execute_code_with_input(self, code_path: str, input_data: str) -> str:
        """
        Виконує Python-код із підміною stdin, повертає те, що було надруковано в stdout.
        """
        with open(code_path, "r", encoding="utf-8") as f:
            code_text = f.read()

        backup_stdin = sys.stdin
        backup_stdout = sys.stdout
        input_buffer = io.StringIO(input_data)
        output_buffer = io.StringIO()

        try:
            sys.stdin = input_buffer
            sys.stdout = output_buffer
            local_env = {}
            exec(code_text, {}, local_env)
        finally:
            sys.stdin = backup_stdin
            sys.stdout = backup_stdout

        return output_buffer.getvalue()

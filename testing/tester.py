import subprocess
from tkinter import messagebox


class Tester:
    """
    Клас для запуску тестів. Для кожного тестового кейсу запускає реальне виконання
    коду (як зовнішній процес) із заданими вхідними даними та порівнює отриманий вивід з очікуваним.
    Якщо програма може бути недетермінованою, кожен запуск виконується окремо (до K разів),
    після кожного запитується у користувача, чи бажає він продовжити запуск наступного варіанту.
    Повертаються докладні результати тестування та відсоток варіантів, що дали правильний результат.
    """

    def run_tests(self, code_path: str, tests: list, k: int = 20):
        overall_results = []
        overall_total_variants = 0
        overall_correct_variants = 0

        for test_case in tests:
            input_data = test_case.get("input", "")
            expected_output = test_case.get("expected_output", "")

            test_log = []
            correct_count = 0
            variant_count = 0

            # Виконуємо запуск до k разів або доки користувач не відмовиться продовжувати
            while variant_count < k:
                result = self._execute_code_with_input(code_path, input_data)
                variant_count += 1

                # 1) Якщо вивід містить рядок "Traceback" або "[Error in", вважаємо що це помилка в коді
                if "Traceback" in result or "[Error in" in result:
                    st = "ERROR"  # або "CODE ERROR"
                    # Можете записати в лог детальніше, що сталася саме помилка в коді
                else:
                    # 2) Якщо це не помилка в коді, тоді порівнюємо з очікуваним виводом
                    if result.strip() == expected_output.strip():
                        st = "OK"
                        correct_count += 1
                    else:
                        st = f"FAIL (expected '{expected_output.strip()}', got '{result.strip()}')"

                # Додаємо запис у лог для кожного запуску
                test_log.append({
                    "variant": variant_count,
                    "status": st,
                    "output": result
                })

                # Якщо ще не досягли максимального числа варіантів, запитуємо користувача
                if variant_count < k:
                    cont = messagebox.askyesno(
                        "Continue Testing",
                        f"Тест з вхідними даними:\n{input_data}\n"
                        f"Варіант #{variant_count}: {st}\n"
                        "Бажаєте виконати ще один варіант?"
                    )
                    if not cont:
                        break

            overall_total_variants += variant_count
            overall_correct_variants += correct_count

            # Відсоток варіантів, що дали правильний результат (відносно k)
            coverage_percent = (correct_count / k) * 100

            overall_results.append({
                "test_input": input_data,
                "expected_output": expected_output,
                "variants_executed": variant_count,
                "correct_variants": correct_count,
                "coverage_percent": coverage_percent,
                "log": test_log
            })

        # Підсумкове покриття:
        # скільки всього варіантів було правильними / (кількість тестів * k)
        overall_coverage = 0
        if tests:
            overall_coverage = (overall_correct_variants / (len(tests) * k)) * 100

        return overall_results, overall_coverage

    def _execute_code_with_input(self, code_path: str, input_data: str) -> str:
        """
        Виконує Python-код як зовнішній процес із підстановкою вхідних даних.
        Об’єднує stderr зі stdout, щоб traceback і повідомлення про помилки
        поверталися разом із нормальним виводом.
        """
        try:
            result = subprocess.run(
                ["python", code_path],
                input=input_data,
                text=True,
                timeout=5,
                stdout=subprocess.PIPE,  # <-- замість capture_output
                stderr=subprocess.STDOUT  # <-- об'єднуємо потоки
            )
            combined_output = result.stdout

            # Якщо код завершився помилкою (ненульовий returncode), додамо позначку
            if result.returncode != 0:
                combined_output = f"[Error in {code_path}]\n{combined_output}"

            return combined_output
        except Exception as e:
            # Наприклад, якщо subprocess.run зірветься по таймауту
            return f"Error during execution: {e}"

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import json
from datetime import datetime

# Імпортуємо наші класи для роботи з тестами
from testing.test_manager import TestManager
from testing.tester import Tester


class TestWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Test Runner and Logs")
        self.geometry("600x500")

        # Екземпляри класів для завантаження тестів та виконання тестування
        self.test_manager = TestManager()  # використовує папку testing/test за замовчуванням
        self.tester = Tester()

        self.code_path = None  # шлях до файлу з кодом для тестування
        self.k_value = 10  # значення K (за замовчуванням)
        self.logs = []  # список лог-записів поточного сеансу

        self.create_widgets()

    def create_widgets(self):
        # Рамка для кнопок керування
        control_frame = tk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        tk.Button(control_frame, text="Load Tests", command=self.load_tests).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Load Code", command=self.load_code).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Set K", command=self.set_k).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Run Tests", command=self.run_tests).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Save Logs", command=self.save_logs).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Load Logs", command=self.load_logs).pack(side=tk.LEFT, padx=5)

        # Рамка для відображення поточного стану (завантажені тести/код)
        status_frame = tk.Frame(self)
        status_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        self.status_label = tk.Label(status_frame, text="No tests or code loaded.")
        self.status_label.pack(side=tk.LEFT, padx=5)

        # Рамка для логування – текстове поле із скролбаром
        log_frame = tk.Frame(self)
        log_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.log_text = tk.Text(log_frame, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

    def add_log(self, message):
        """Додає запис у лог (як у текстове поле, так і у внутрішній список) з міткою часу."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {"timestamp": timestamp, "message": message}
        self.logs.append(log_entry)
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def load_tests(self):
        """Завантаження тестів із папки testing/test або через діалогове вікно."""
        found_tests = self.test_manager.find_existing_tests()
        if found_tests:
            # Завантажуємо перший знайдений JSON
            self.test_manager.load_tests_from_json(found_tests[0])
            self.add_log(f"Loaded tests from: {found_tests[0]}")
            self.status_label.config(text=f"Tests loaded: {os.path.basename(found_tests[0])}")
        else:
            file_path = filedialog.askopenfilename(
                title="Select JSON test file",
                initialdir=os.path.join(os.getcwd(), "testing", "test"),
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if file_path:
                self.test_manager.load_tests_from_json(file_path)
                self.add_log(f"Loaded tests from: {file_path}")
                self.status_label.config(text=f"Tests loaded: {os.path.basename(file_path)}")

    def load_code(self):
        """Завантаження файлу з кодом для тестування."""
        file_path = filedialog.askopenfilename(
            title="Select code file to test",
            filetypes=[("Python files", "*.py *.txt"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )
        if file_path:
            self.code_path = file_path
            self.add_log(f"Loaded code file: {file_path}")
            self.status_label.config(text=f"Code loaded: {os.path.basename(file_path)}")

    def set_k(self):
        """Встановлення значення K для тестування."""
        k_value = simpledialog.askinteger("Set K", "Enter K (1 <= K <= 20):", parent=self, minvalue=1, maxvalue=20)
        if k_value:
            self.k_value = k_value
            self.add_log(f"Set K to {k_value}")

    def run_tests(self):
        """
        Запускає тестування: перевіряє, що завантажено тести та код, запускає тести та логування результатів.
        """
        if not self.test_manager.tests_loaded():
            self.add_log("No tests loaded. Please load tests first.")
            return
        if not self.code_path:
            self.add_log("No code file loaded. Please load a code file to test.")
            return

        self.add_log("Starting tests...")
        try:
            # Отримуємо загальний список результатів (по тестах) і сумарний coverage
            test_results, coverage_percent = self.tester.run_tests(
                code_path=self.code_path,
                tests=self.test_manager.get_tests(),
                k=self.k_value
            )

            # Підрахуємо загальну кількість "OK" по всіх варіантах усіх тестів
            passed_count = 0
            total_variants = 0

            for test_data in test_results:
                for variant_info in test_data["log"]:
                    total_variants += 1
                    if variant_info["status"] == "OK":
                        passed_count += 1

            # Формуємо загальний підсумок
            summary = (
                f"Test Summary:\n"
                f"Passed (OK): {passed_count} / {total_variants}\n"
                f"Coverage for <= {self.k_value} steps: {coverage_percent:.2f}%"
            )
            self.add_log(summary)

            # Детальний лог по кожному тесту
            for i, test_data in enumerate(test_results, start=1):
                self.add_log(f"Test #{i}: executed {test_data['variants_executed']} variants, "
                             f"correct: {test_data['correct_variants']}, "
                             f"coverage: {test_data['coverage_percent']:.2f}%")
                # Перебираємо кожен запуск (варіант)
                for variant_info in test_data["log"]:
                    var_num = variant_info["variant"]
                    var_status = variant_info["status"]
                    var_output = variant_info["output"].strip()
                    self.add_log(f"  Variant #{var_num}: {var_status} (output: {var_output})")

        except Exception as e:
            self.add_log(f"Error during testing: {str(e)}")

    def save_logs(self):
        """Зберігає логи поточного сеансу у JSON-файл (початкова папка testing/test)."""
        file_path = filedialog.asksaveasfilename(
            title="Save Logs",
            initialdir=os.path.join(os.getcwd(), "testing", "test"),
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.logs, f, indent=4, ensure_ascii=False)
                self.add_log(f"Logs saved to {file_path}")
            except Exception as e:
                self.add_log(f"Error saving logs: {str(e)}")

    def load_logs(self):
        """Завантажує логи з JSON-файлу та відображає їх у лог-вікні."""
        file_path = filedialog.askopenfilename(
            title="Load Logs",
            initialdir=os.path.join(os.getcwd(), "testing", "test"),
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    loaded_logs = json.load(f)
                self.logs = loaded_logs
                self.log_text.delete(1.0, tk.END)
                for entry in self.logs:
                    self.log_text.insert(tk.END, f"[{entry['timestamp']}] {entry['message']}\n")
                self.add_log(f"Logs loaded from {file_path}")
            except Exception as e:
                self.add_log(f"Error loading logs: {str(e)}")

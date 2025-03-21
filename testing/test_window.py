import customtkinter as ctk
from tkinter import filedialog
import os
import json
from datetime import datetime

# Імпортуємо класи для роботи з тестами
from testing.test_manager import TestManager
from testing.tester import Tester

# Налаштовуємо глобальний стиль CustomTkinter
ctk.set_appearance_mode("dark")  # Використовуємо темний режим
ctk.set_default_color_theme("blue")  # Темна палітра з синім акцентом (натхненна VSCode)


class TestWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Test Runner and Logs")
        self.geometry("800x650")
        self.attributes("-alpha", 0.95)  # 95% непрозорості

        # Робимо вікно модальним
        self.transient(master)
        self.grab_set()
        self.focus_force()

        # Екземпляри класів для роботи з тестами
        self.test_manager = TestManager()  # використовує папку testing/test за замовчуванням
        self.tester = Tester()

        self.code_path = None  # шлях до файлу з кодом для тестування
        self.k_value = 10  # значення K (за замовчуванням)
        self.logs = []  # список лог-записів поточного сеансу

        self.create_widgets()

    def create_widgets(self):
        # Рамка для кнопок керування
        control_frame = ctk.CTkFrame(self, corner_radius=8)
        control_frame.pack(side="top", fill="x", padx=15, pady=15)

        ctk.CTkButton(control_frame, text="Load Tests", command=self.load_tests, width=120).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="Load Code", command=self.load_code, width=120).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="Set K", command=self.set_k, width=120).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="Run Tests", command=self.run_tests, width=120).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="Save Logs", command=self.save_logs, width=120).pack(side="left", padx=5)
        ctk.CTkButton(control_frame, text="Load Logs", command=self.load_logs, width=120).pack(side="left", padx=5)

        # Рамка для статусу
        status_frame = ctk.CTkFrame(self, corner_radius=8)
        status_frame.pack(side="top", fill="x", padx=15, pady=(0, 10))
        self.status_label = ctk.CTkLabel(status_frame, text="No tests or code loaded.", font=("Segoe UI", 12))
        self.status_label.pack(side="left", padx=10, pady=10)

        # Рамка для логування – текстове поле із скролбаром
        log_frame = ctk.CTkFrame(self, corner_radius=8)
        log_frame.pack(side="top", fill="both", expand=True, padx=15, pady=15)
        # Збільшуємо розмір шрифту для логів (наприклад, 14)
        self.log_text = ctk.CTkTextbox(log_frame, corner_radius=8, font=("Segoe UI", 14))
        self.log_text.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar = ctk.CTkScrollbar(log_frame, orientation="vertical", command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        self.log_text.configure(yscrollcommand=scrollbar.set)

    def add_log(self, message):
        """Додає запис у лог із міткою часу."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {"timestamp": timestamp, "message": message}
        self.logs.append(log_entry)
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")

    def load_tests(self):
        """Завантаження тестів із папки testing/test або через діалогове вікно."""
        found_tests = self.test_manager.find_existing_tests()
        if found_tests:
            self.test_manager.load_tests_from_json(found_tests[0])
            self.add_log(f"Loaded tests from: {found_tests[0]}")
            self.status_label.configure(text=f"Tests loaded: {os.path.basename(found_tests[0])}")
        else:
            file_path = filedialog.askopenfilename(
                title="Select JSON test file",
                initialdir=os.path.join(os.getcwd(), "testing", "test"),
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if file_path:
                self.test_manager.load_tests_from_json(file_path)
                self.add_log(f"Loaded tests from: {file_path}")
                self.status_label.configure(text=f"Tests loaded: {os.path.basename(file_path)}")

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
            self.status_label.configure(text=f"Code loaded: {os.path.basename(file_path)}")

    def set_k(self):
        """Встановлення значення K для тестування за допомогою CTkInputDialog."""
        # Використовуємо CTkInputDialog для отримання нового значення K
        dialog = ctk.CTkInputDialog(text="Enter K (1 <= K <= 20):", title="Set K")
        result = dialog.get_input()  # отримуємо рядок
        try:
            k_value = int(result)
            if 1 <= k_value <= 20:
                self.k_value = k_value
                self.add_log(f"Set K to {k_value}")
            else:
                self.add_log("Invalid value for K. Must be between 1 and 20.")
        except (ValueError, TypeError):
            self.add_log("Invalid input for K.")

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
            test_results, coverage_percent = self.tester.run_tests(
                code_path=self.code_path,
                tests=self.test_manager.get_tests(),
                k=self.k_value
            )

            passed_count = 0
            total_variants = 0

            for test_data in test_results:
                for variant_info in test_data["log"]:
                    total_variants += 1
                    if variant_info["status"] == "OK":
                        passed_count += 1

            summary = (
                f"Test Summary:\n"
                f"Passed (OK): {passed_count} / {total_variants}\n"
                f"Coverage for <= {self.k_value} steps: {coverage_percent:.2f}%"
            )
            self.add_log(summary)

            for i, test_data in enumerate(test_results, start=1):
                self.add_log(f"Test #{i}: executed {test_data['variants_executed']} variants, "
                             f"correct: {test_data['correct_variants']}, "
                             f"coverage: {test_data['coverage_percent']:.2f}%")
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
                self.log_text.delete("1.0", "end")
                for entry in self.logs:
                    self.log_text.insert("end", f"[{entry['timestamp']}] {entry['message']}\n")
                self.add_log(f"Logs loaded from {file_path}")
            except Exception as e:
                self.add_log(f"Error loading logs: {str(e)}")


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("800x600")
    app.title("Main Window")


    def open_test_window():
        TestWindow(master=app)


    btn = ctk.CTkButton(app, text="Open Test Window", command=open_test_window)
    btn.pack(padx=20, pady=20)
    app.mainloop()

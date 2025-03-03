import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from .diagram_editor import DiagramEditor
from .shared_variables import SharedVariables
from testing.code_runner import CodeRunner
from testing.test_manager import TestManager
from testing.tester import Tester

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Multi-threaded Block Diagram Editor")
        self.root.geometry("800x600")
        self.code_runner = CodeRunner()
        self.test_manager = TestManager()
        self.tester = Tester()
        self.shared_variables = SharedVariables(self.update_variable_list)
        self.init_ui()

    def init_ui(self):
        # Рядок команд

        command_frame = tk.Frame(self.root)
        command_frame.pack(side=tk.TOP, fill=tk.X)

        save_button = tk.Button(command_frame, text="Save", command=self.save)
        save_button.pack(side=tk.LEFT, padx=5, pady=5, ipadx=8)

        open_button = tk.Button(command_frame, text="Open", command=self.open_file)
        open_button.pack(side=tk.LEFT, padx=5, pady=5, ipadx=8)

        run_button = tk.Button(command_frame, text="Run", command=self.run_code)
        run_button.pack(side=tk.LEFT, padx=5, pady=5, ipadx=8)

        test_button = tk.Button(command_frame, text="Test", command=self.test)
        test_button.pack(side=tk.LEFT, padx=5, pady=5, ipadx=8)

        exit_button = tk.Button(command_frame, text="Exit", command=self.exit_program)
        exit_button.pack(side=tk.RIGHT, padx=5, pady=5, ipadx=8)

        new_page_button = tk.Button(command_frame, text="New page", command=self.new_page)
        new_page_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Фрейм для управління змінними
        variable_frame = tk.Frame(self.root)
        variable_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        tk.Label(variable_frame, text="Shared Variables:").pack()

        self.variable_listbox = tk.Listbox(variable_frame, height=15)
        self.variable_listbox.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(variable_frame)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Add", command=self.add_variable).pack(side=tk.LEFT, fill=tk.X, pady=10, expand=True)
        tk.Button(btn_frame, text="Edit", command=self.edit_variable).pack(side=tk.LEFT, fill=tk.X, pady=10, expand=True)
        tk.Button(btn_frame, text="Delete", command=self.delete_variable).pack(side=tk.LEFT, fill=tk.X, pady=10, expand=True)

        self.update_variable_list()

        # Вкладки для потоків
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Додавання першого потоку за замовчуванням
        self.page_count = 0
        self.new_page()

    def save(self):
        """Порожня функція для Save"""
        print("Save functionality is not implemented yet.")

    def open_file(self):
        """Порожня функція для Open"""
        print("Open functionality is not implemented yet.")

        # -------------------------------------------------------------------------
        # Реалізація "Run Code"
        # -------------------------------------------------------------------------

    def run_code(self):
        """
        1) Відкрити діалогове вікно для вибору файлу з кодом.
        2) Запитати у користувача вхідні дані, якщо код їх очікує.
        3) Виконати код через CodeRunner і показати результат.
        """
        file_path = filedialog.askopenfilename(
            title="Select Python Code",
            filetypes=[("Python files", "*.py *.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return  # Користувач скасував вибір файлу

        # Запитуємо вхідні дані у користувача (можна залишити порожнім, якщо не потрібно)
        input_data = simpledialog.askstring("Input Data",
                                            "Введіть вхідні дані для програми (якщо потрібно):",
                                            parent=self.root)
        if input_data is None:
            input_data = ""  # Якщо користувач скасував, використовуємо порожній рядок

        try:
            output = self.code_runner.run_file(file_path, input_data)
            messagebox.showinfo("Run Code", f"Output:\n{output}")
        except Exception as e:
            messagebox.showerror("Run Code Error", str(e))

    def test(self):
        """
        Натискання кнопки "Test" відкриває вікно для тестування та логування.
        """
        from testing.test_window import TestWindow
        test_window = TestWindow(self.root)

    def exit_program(self):
        """Підтвердження перед закриттям програми"""
        confirm = messagebox.askyesnocancel(
            "Exit",
            "Changes are not saved. Do you want to save before exiting?"
        )
        if confirm is None:  # Cancel
            return
        elif confirm:  # Yes
            self.save()
        self.root.quit()  # Exit the application

    def new_page(self):
        """Додати нову вкладку для потоку"""
        self.page_count += 1
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text=f"Page {self.page_count}")

        # Полотно для блок-схеми
        editor = DiagramEditor(tab, self.shared_variables)
        editor.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()

    def add_variable(self):
        name = simpledialog.askstring("Add Variable", "Enter variable name:", parent=self.root)
        if not name:
            return

        value = simpledialog.askinteger("Add Variable", f"Enter initial value for {name}:", parent=self.root)
        if value is None:  # Якщо користувач натиснув "Скасувати"
            return

        if self.shared_variables.add_variable(name, value):
            self.update_variable_list()
        else:
            messagebox.showerror("Error", "Variable limit reached or name already exists.")

    def edit_variable(self):
        selected = self.variable_listbox.curselection()
        if not selected:
            return
        var_name = self.variable_listbox.get(selected[0]).split(" = ")[0]  # Отримуємо ім'я змінної
        new_value = simpledialog.askinteger("Edit Variable", f"Enter new value for {var_name}:", parent=self.root)
        if new_value is not None:
            self.shared_variables.update_variable(var_name, new_value)
            self.update_variable_list()

    def delete_variable(self):
        selected = self.variable_listbox.curselection()
        if not selected:
            return
        var_name = self.variable_listbox.get(selected[0]).split(" = ")[0]  # Отримуємо ім'я змінної
        if self.shared_variables.remove_variable(var_name):
            self.update_variable_list()

    def update_variable_list(self):
        """Оновлює список змінних у GUI."""
        self.variable_listbox.delete(0, tk.END)
        for var_name, value in self.shared_variables.get_variables().items():
            self.variable_listbox.insert(tk.END, f"{var_name} = {value}")
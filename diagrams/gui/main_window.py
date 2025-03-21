import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from .diagram_editor import DiagramEditor
from .shared_variables import SharedVariables
from testing.code_runner import CodeRunner
from testing.test_manager import TestManager
from testing.tester import Tester
from .blocks.StartBlock import StartBlock
import json
from .diagram import Diagram

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Багатопотоковий редактор блок-схем")
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

        save_button = tk.Button(command_frame, text="Зберегти", command=self.save)
        save_button.pack(side=tk.LEFT, padx=5, pady=5, ipadx=8)

        open_button = tk.Button(command_frame, text="Відкрити", command=self.open_file)
        open_button.pack(side=tk.LEFT, padx=5, pady=5, ipadx=8)

        run_button = tk.Button(command_frame, text="Запустити", command=self.run_code)
        run_button.pack(side=tk.LEFT, padx=5, pady=5, ipadx=8)

        test_button = tk.Button(command_frame, text="Test", command=self.test)

        test_button.pack(side=tk.LEFT, padx=5, pady=5, ipadx=8)

        exit_button = tk.Button(command_frame, text="Вихід", command=self.exit_program)
        exit_button.pack(side=tk.RIGHT, padx=5, pady=5, ipadx=8)

        new_page_button = tk.Button(command_frame, text="Нова сторінка", command=self.new_page)
        new_page_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Фрейм для управління змінними
        variable_frame = tk.Frame(self.root)
        variable_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        tk.Label(variable_frame, text="Спільні змінні:").pack()

        self.variable_listbox = tk.Listbox(variable_frame, height=15)
        self.variable_listbox.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(variable_frame)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Додати", command=self.add_variable).pack(side=tk.LEFT, fill=tk.X, pady=10, expand=True)
        tk.Button(btn_frame, text="Редагувати", command=self.edit_variable).pack(side=tk.LEFT, fill=tk.X, pady=10, expand=True)
        tk.Button(btn_frame, text="Видалити", command=self.delete_variable).pack(side=tk.LEFT, fill=tk.X, pady=10, expand=True)

        self.update_variable_list()

        # Вкладки для потоків
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Додавання першого потоку за замовчуванням
        self.page_count = 0
        self.new_page()

    def save(self):
        """Зберігає всі діаграми у JSON-файли."""
        for i, tab in enumerate(self.tabs.winfo_children()):
            # Отримуємо об'єкт DiagramEditor з вкладки
            for widget in tab.winfo_children():
                if isinstance(widget, DiagramEditor):
                    diagram = widget.diagram
                    filename = filedialog.asksaveasfilename(
                        defaultextension=".json",
                        filetypes=[("JSON Files", "*.json")],
                        initialfile=f"{diagram.name}.json"
                    )
                    if filename:
                        with open(filename, "w", encoding="utf-8") as file:
                            json.dump(diagram.to_dict(), file, indent=4, ensure_ascii=False)

    def open_file(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if not filename:
            return

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        tab = ttk.Frame(self.tabs)
        diagram_name = data["name"]
        self.tabs.add(tab, text=diagram_name)
        editor = DiagramEditor(tab, self.shared_variables, diagram_name)
        editor.pack(fill=tk.BOTH, expand=True)
        editor.diagram.load_from_dict(data, editor)
        editor.diagram.render(editor)

        self.update_variable_list()  # Оновити панель змінних

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
            "Вихід",
            "Зміни не зберігаються. Ви хочете зберегти зміни перед виходом?"
        )
        if confirm is None:  # Cancel
            return
        elif confirm:  # Yes
            self.save()
        self.root.quit()  # Exit the application

    def new_page(self):
        """Додати нову вкладку для потоку та автоматично додає блок Початок"""
        self.page_count += 1
        tab = ttk.Frame(self.tabs)
        diagram_name = f"Diagram_{self.page_count}"
        self.tabs.add(tab, text=diagram_name)

        # Полотно для блок-схеми
        editor = DiagramEditor(tab, self.shared_variables, diagram_name)
        editor.pack(fill=tk.BOTH, expand=True)

        # Додаємо блок "Початок" автоматично
        start_block = StartBlock(block_id=1, x=250, y=50, shared_variables=self.shared_variables, parent=editor)
        editor.diagram.add_block(start_block)
        editor.diagram.render(editor)

    def run(self):
        self.root.mainloop()

    def add_variable(self):
        name = simpledialog.askstring("Додати змінну", "Введіть назву змінної:", parent=self.root)
        if not name:
            return

        value = simpledialog.askinteger("Додати змінну", f"Введіть початкове значення для {name}:", parent=self.root)
        if value is None:  # Якщо користувач натиснув "Скасувати"
            return

        if self.shared_variables.add_variable(name, value):
            self.update_variable_list()
        else:
            messagebox.showerror("Помилка.", "Ліміт досягнуто або ім'я вже існує.")

    def edit_variable(self):
        selected = self.variable_listbox.curselection()
        if not selected:
            return
        var_name = self.variable_listbox.get(selected[0]).split(" = ")[0]  # Отримуємо ім'я змінної
        new_value = simpledialog.askinteger("Редагування змінної", f"Введіть нове значення для {var_name}:", parent=self.root)
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
import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
import os
import json

from .diagram_editor import DiagramEditor
from .shared_variables import SharedVariables
from testing.code_runner import CodeRunner
from testing.test_manager import TestManager
from testing.tester import Tester
from .blocks.StartBlock import StartBlock
from .diagram import Diagram
from translation.thread import Thread
from translation.code_writer import Writer

# Налаштовуємо глобальний стиль CustomTkinter:
ctk.set_appearance_mode("dark")  # темний режим
ctk.set_default_color_theme("dark-blue")  # сучасна темна палітра із синім акцентом


class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()  # Використовуємо CTk замість стандартного tk.Tk()
        self.root.title("Багатопотоковий редактор блок-схем")
        self.root.geometry("1200x600")

        self.code_runner = CodeRunner()
        self.test_manager = TestManager()
        self.tester = Tester()
        self.shared_variables = SharedVariables(self.update_variable_list)

        self.init_ui()

    def init_ui(self):
        # Рядок команд
        command_frame = ctk.CTkFrame(self.root, corner_radius=8)
        command_frame.pack(side="top", fill="x", padx=10, pady=10)

        save_button = ctk.CTkButton(command_frame, text="Зберегти", command=self.save, width=120)
        save_button.pack(side="left", padx=5, pady=5)

        open_button = ctk.CTkButton(command_frame, text="Відкрити", command=self.open_file, width=120)
        open_button.pack(side="left", padx=5, pady=5)

        run_button = ctk.CTkButton(command_frame, text="Запустити", command=self.run_code, width=120)
        run_button.pack(side="left", padx=5, pady=5)

        test_button = ctk.CTkButton(command_frame, text="Test", command=self.test, width=120)
        test_button.pack(side="left", padx=5, pady=5)

        exit_button = ctk.CTkButton(command_frame, text="Вихід", command=self.exit_program, width=120)
        exit_button.pack(side="right", padx=5, pady=5)

        new_page_button = ctk.CTkButton(command_frame, text="Нова сторінка", command=self.new_page, width=120)
        new_page_button.pack(side="right", padx=5, pady=5)

        # Фрейм для управління змінними (зменшено висоту текстового поля)
        variable_frame = ctk.CTkFrame(self.root, corner_radius=8)
        variable_frame.pack(side="right", fill="y", padx=10, pady=10)

        var_label = ctk.CTkLabel(variable_frame, text="Спільні змінні:", font=("Segoe UI", 12))
        var_label.pack(pady=(0, 5))

        self.variable_listbox = ctk.CTkTextbox(variable_frame, height=80, font=("Segoe UI", 12))
        self.variable_listbox.pack(fill="both", expand=True)

        btn_frame = ctk.CTkFrame(variable_frame, corner_radius=8)
        btn_frame.pack(fill="x", pady=10)

        add_button = ctk.CTkButton(btn_frame, text="Додати", command=self.add_variable)
        add_button.pack(side="left", fill="x", expand=True, padx=2)
        edit_button = ctk.CTkButton(btn_frame, text="Редагувати", command=self.edit_variable)
        edit_button.pack(side="left", fill="x", expand=True, padx=2)
        del_button = ctk.CTkButton(btn_frame, text="Видалити", command=self.delete_variable)
        del_button.pack(side="left", fill="x", expand=True, padx=2)

        self.update_variable_list()

        # Вкладки для потоків – CTkTabview
        self.tabs = ctk.CTkTabview(self.root)
        self.tabs.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.page_count = 0
        self.new_page()

    def save(self):
        """Зберігає всі діаграми у JSON-файли."""
        # Використовуємо внутрішній словник вкладок
        for tab_name in list(self.tabs._tab_dict.keys()):
            tab = self.tabs._tab_dict[tab_name]
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
        diagram_name = data["name"]
        unique_name = diagram_name
        counter = 1
        while unique_name in self.tabs._tab_dict:
            unique_name = f"{diagram_name}_{counter}"
            counter += 1
        self.tabs.add(unique_name)
        tab = self.tabs.tab(unique_name)
        editor = DiagramEditor(tab, self.shared_variables, unique_name)
        editor.pack(fill="both", expand=True)
        editor.diagram.load_from_dict(data, editor)
        editor.diagram.render(editor)
        self.update_variable_list()

    def run_code(self):
        json_dir = os.path.join(
            os.path.dirname(__file__),
            '..', '..',
            'translation',
            'diagramJson'
        )
        json_files = [os.path.join(json_dir, file) for file in os.listdir(json_dir) if file.endswith(".json")]
        shared_variables = {}
        threads = []
        for filename in json_files:
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                shared_variables.update(data.get("shared_variables", {}))
                thread = Thread(thread_id=data["name"], shared_vars=shared_variables)
                thread.build_from_json(data)
                threads.append(thread)
            except Exception as e:
                print(f"Помилка при обробці файлу {filename}: {e}")
        writer = Writer("generated_code.py")
        writer.write_code(threads, shared_variables)
        print("Код згенеровано у файлі 'generated_code.py'")

    def test(self):
        """
        Натискання кнопки "Test" відкриває вікно для тестування та логування.
        """
        from testing.test_window import TestWindow
        test_window = TestWindow(self.root)

    def exit_program(self):
        confirm = messagebox.askyesnocancel(
            "Вихід",
            "Зміни не зберігаються. Ви хочете зберегти зміни перед виходом?"
        )
        if confirm is None:
            return
        elif confirm:
            self.save()
        self.root.quit()

    def new_page(self):
        self.page_count += 1
        diagram_name = f"Diagram_{self.page_count}"
        unique_name = diagram_name
        counter = 1
        while unique_name in self.tabs._tab_dict:
            unique_name = f"{diagram_name}_{counter}"
            counter += 1
        self.tabs.add(unique_name)
        tab = self.tabs.tab(unique_name)
        editor = DiagramEditor(tab, self.shared_variables, unique_name)
        editor.pack(fill="both", expand=True)
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
        if value is None:
            return
        if self.shared_variables.add_variable(name, value):
            self.update_variable_list()
        else:
            messagebox.showerror("Помилка", "Ліміт досягнуто або ім'я вже існує.")

    def edit_variable(self):
        """
        Пропонує користувачу вибрати змінну з випадаючого списку,
        а потім ввести нове значення для неї.
        """
        # Зчитуємо всі рядки з CTkTextbox
        lines = self.variable_listbox.get("1.0", "end").splitlines()
        if not lines:
            return

        # Витягаємо імена змінних із кожного рядка
        variable_names = []
        for line in lines:
            if " = " in line:
                var_name = line.split(" = ")[0].strip()
                variable_names.append(var_name)

        if not variable_names:
            return  # Немає змінних для редагування

        # Створюємо тимчасове вікно для вибору змінної
        top = ctk.CTkToplevel(self.root)
        top.title("Оберіть змінну для редагування")
        top.grab_set()  # робимо вікно модальним

        label = ctk.CTkLabel(top, text="Оберіть змінну:", font=("Segoe UI", 12))
        label.pack(padx=20, pady=(20, 10))

        # Використовуємо CTkOptionMenu, щоб відобразити імена змінних
        var_name_var = ctk.StringVar(value=variable_names[0])  # за замовчуванням перша змінна
        option_menu = ctk.CTkOptionMenu(top, variable=var_name_var, values=variable_names)
        option_menu.pack(padx=20, pady=10)

        def confirm():
            selected_var = var_name_var.get()
            top.destroy()
            # Запитуємо нове значення для обраної змінної
            new_value = simpledialog.askinteger("Редагування змінної",
                                                f"Введіть нове значення для {selected_var}:",
                                                parent=self.root)
            if new_value is not None:
                self.shared_variables.update_variable(selected_var, new_value)
                self.update_variable_list()

        ok_button = ctk.CTkButton(top, text="OK", command=confirm)
        ok_button.pack(pady=(0, 20))

        # Центруємо вікно над головним
        top.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - top.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - top.winfo_height()) // 2
        top.geometry(f"+{x}+{y}")

    def delete_variable(self):
        lines = self.variable_listbox.get("1.0", "end").splitlines()
        if not lines:
            return
        var_name = lines[0].split(" = ")[0]
        if self.shared_variables.remove_variable(var_name):
            self.update_variable_list()

    def update_variable_list(self):
        self.variable_listbox.delete("1.0", "end")
        for var_name, value in self.shared_variables.get_variables().items():
            self.variable_listbox.insert("end", f"{var_name} = {value}\n")


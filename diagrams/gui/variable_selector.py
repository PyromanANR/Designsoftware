import tkinter as tk
from tkinter import messagebox, ttk

class VariableSelector:
    def __init__(self, parent, shared_variables):
        self.parent = parent
        self.shared_variables = shared_variables

    def select_variable(self, title="Виберіть змінну"):
        """Вибір змінної з існуючих у списку"""
        variables = self.shared_variables.get_variables()

        if not variables:
            messagebox.showerror("Ще немає створених змінних", "Будь ласка, створіть принаймні одну спільну змінну перед використанням цього блоку.")
            return None

        return self._show_selection_window(title, list(variables.keys()))

    def select_two_variables(self):
        """Вибір двох змінних (для блоків присвоєння V1 = V2)"""
        variables = self.shared_variables.get_variables()

        if len(variables) < 2:
            messagebox.showerror("Недостатньо змінних", "Будь ласка, створіть принаймні дві спільні змінні перед використанням цього блоку.")
            return None, None

        var1 = self._show_selection_window("Виберіть Змінну 1", list(variables.keys()))
        var2 = self._show_selection_window("Виберіть Змінну 2", list(variables.keys()))

        while var1 == var2:  # Забороняємо вибирати одну і ту ж змінну двічі
            messagebox.showerror("Дублююча змінна", "Будь ласка, оберіть дві різні змінні.")
            var2 = self._show_selection_window("Виберіть Змінну 2", list(variables.keys()))

        return var1, var2

    def _show_selection_window(self, title, variable_list):
        """Показує випадаючий список для вибору змінної"""
        var_window = tk.Toplevel(self.parent)
        var_window.title(title)

        tk.Label(var_window, text="Виберіть змінну:").pack(padx=10, pady=5)

        var_choice = tk.StringVar()
        var_combobox = ttk.Combobox(var_window, textvariable=var_choice, values=variable_list, state="readonly")
        var_combobox.pack(padx=10, pady=5)
        var_combobox.current(0)  # Встановлюємо першу змінну за замовчуванням

        def confirm():
            var_window.selected_var = var_choice.get()
            var_window.destroy()

        tk.Button(var_window, text="OK", command=confirm).pack(pady=5)
        var_window.selected_var = None
        var_window.wait_window()

        return var_window.selected_var
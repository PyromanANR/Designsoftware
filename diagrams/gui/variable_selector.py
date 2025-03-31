import customtkinter as ctk
from tkinter import messagebox

class VariableSelector:
    def __init__(self, parent, shared_variables):
        self.parent = parent
        self.shared_variables = shared_variables

    def select_variable(self, title="Виберіть змінну"):
        variables = self.shared_variables.get_variables()

        if not variables:
            messagebox.showerror("Ще немає створених змінних", "Будь ласка, створіть принаймні одну спільну змінну перед використанням цього блоку.")
            return None

        return self._show_selection_window(title, list(variables.keys()))

    def select_two_variables(self):
        variables = self.shared_variables.get_variables()

        if len(variables) < 2:
            messagebox.showerror("Недостатньо змінних", "Будь ласка, створіть принаймні дві спільні змінні перед використанням цього блоку.")
            return None, None

        var1 = self._show_selection_window("Виберіть Змінну 1", list(variables.keys()))
        var2 = self._show_selection_window("Виберіть Змінну 2", list(variables.keys()))

        while var1 == var2:
            messagebox.showerror("Дублююча змінна", "Будь ласка, оберіть дві різні змінні.")
            var2 = self._show_selection_window("Виберіть Змінну 2", list(variables.keys()))

        return var1, var2

    def _show_selection_window(self, title, variable_list):
        window = ctk.CTkToplevel(self.parent)
        window.title(title)
        window.geometry("300x160")
        window.grab_set()
        window.resizable(False, False)

        ctk.CTkLabel(window, text="Виберіть змінну:", font=("Segoe UI", 12)).pack(pady=(20, 5))

        var_choice = ctk.StringVar(value=variable_list[0])
        dropdown = ctk.CTkOptionMenu(window, variable=var_choice, values=variable_list)
        dropdown.pack(pady=5)

        result = {"selected": None}

        def confirm():
            result["selected"] = var_choice.get()
            window.destroy()

        ctk.CTkButton(window, text="OK", command=confirm).pack(pady=(15, 10))

        # Центрування
        window.update_idletasks()
        x = self.parent.winfo_rootx() + (self.parent.winfo_width() - window.winfo_width()) // 2
        y = self.parent.winfo_rooty() + (self.parent.winfo_height() - window.winfo_height()) // 2
        window.geometry(f"+{x}+{y}")

        window.wait_window()
        return result["selected"]

import tkinter as tk
from tkinter import simpledialog


import customtkinter as ctk

class BlockOptionsDialog(ctk.CTkToplevel):
    def __init__(self, parent, title="Виберіть тип блоку"):
        super().__init__(parent)
        self.title(title)
        self.geometry("360x400")
        self.grab_set()
        self.resizable(False, False)

        self.selected_option = None
        self.var = ctk.StringVar(value="Assignment (V1 = V2)")

        ctk.CTkLabel(self, text="Оберіть тип блоку:", font=("Segoe UI", 14)).pack(pady=(20, 10))

        options = [
            "Assignment (V1 = V2)",
            "Constant (V = C)",
            "Input (INPUT V)",
            "Output (PRINT V)",
            "Condition (V == C)",
            "Condition (V < C)",
            "End"
        ]

        for option in options:
            ctk.CTkRadioButton(self, text=option, variable=self.var, value=option).pack(anchor="w", padx=40, pady=4)

        ctk.CTkButton(self, text="OK", command=self.on_confirm).pack(pady=(20, 10))

        # Центрування
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def on_confirm(self):
        self.selected_option = self.var.get()
        self.destroy()


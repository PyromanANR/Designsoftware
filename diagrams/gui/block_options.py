import tkinter as tk
from tkinter import simpledialog

class BlockOptionsDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.selected_option = None
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Select block type:").grid(row=0, column=0, padx=10, pady=10)

        self.var = tk.StringVar(value="Assignment")
        options = ["Assignment (V1 = V2)", "Constant (V = C)", "Input (INPUT V)", "Output (PRINT V)", "Condition (V == C)", "Condition (V < C)"]
        for i, option in enumerate(options):
            tk.Radiobutton(master, text=option, variable=self.var, value=option).grid(row=i + 1, column=0, sticky="w", padx=20)

    def apply(self):
        self.selected_option = self.var.get()
#Головне вікно програми
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from diagrams.gui.diagram_editor import DiagramEditor

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Multi-threaded Block Diagram Editor")
        self.root.geometry("800x600")

        self.init_ui()

    def init_ui(self):
        # Рядок команд
        command_frame = tk.Frame(self.root)
        command_frame.pack(side=tk.TOP, fill=tk.X)

        # Команда Save
        save_button = tk.Button(command_frame, text="Save", command=self.save)
        save_button.pack(side=tk.LEFT, padx=5, pady=5, ipadx=8)

        # Команда Open
        open_button = tk.Button(command_frame, text="Open", command=self.open_file)
        open_button.pack(side=tk.LEFT, padx=5, pady=5, ipadx=8)

        # Команда Exit
        exit_button = tk.Button(command_frame, text="Exit", command=self.exit_program)
        exit_button.pack(side=tk.LEFT, padx=5, pady=5, ipadx=8)

        # Команда New page
        exit_button = tk.Button(command_frame, text="New page", command=self.new_page)
        exit_button.pack(side=tk.RIGHT, padx=5, pady=5)

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
        editor = DiagramEditor(tab)
        editor.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()
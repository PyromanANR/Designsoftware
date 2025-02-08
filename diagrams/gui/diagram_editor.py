import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from .block_options import BlockOptionsDialog, AssignmentBlock, ConstantBlock, InputBlock, OutputBlock, ConditionBlock

class Diagram:
    def __init__(self):
        self.blocks = []

    def add_block(self, block):
        self.blocks.append(block)

    def render(self, canvas):
        for block in self.blocks:
            block.render(canvas)

class DiagramEditor(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="white", width=600, height=400)
        self.pack(fill=tk.BOTH, expand=True)
        self.diagram = Diagram()

        #self.blocks = []  # Список блоків
        self.current_block = None  # Поточний блок, який перетягують
        self.offset_x = 0  # Зміщення миші по X
        self.offset_y = 0  # Зміщення миші по Y

        self.bind("<Double-1>", self.add_block)  # Подвійний клік для додавання блоку
        self.bind("<Button-1>", self.on_block_click)  # Натискання для вибору блоку
        self.bind("<B1-Motion>", self.on_block_drag)  # Перетягування блоку
        self.bind("<ButtonRelease-1>", self.on_block_release)  # Завершення перетягування

    def add_block(self, event):
        """Додає блок з вибором типу після кліку"""
        block_id = len(self.diagram.blocks) + 1
        dialog = BlockOptionsDialog(self, title="Select Block Type")
        block_type = dialog.selected_option
        if block_type is None:  # Якщо користувач закрив діалогове вікно
            return

        if block_type == "Assignment (V1 = V2)":
            var1 = simpledialog.askstring("Input", "Enter variable 1:", parent=self)
            var2 = simpledialog.askstring("Input", "Enter variable 2:", parent=self)
            block = AssignmentBlock(block_id, event.x, event.y, var1, var2)
        elif block_type == "Constant (V = C)":
            var = simpledialog.askstring("Input", "Enter variable:", parent=self)
            value = simpledialog.askstring("Input", "Enter value:", parent=self)
            block = ConstantBlock(block_id, event.x, event.y, var, value)
        elif block_type == "Input (INPUT V)":
            var = simpledialog.askstring("Input", "Enter variable:", parent=self)
            block = InputBlock(block_id, event.x, event.y, var)
        elif block_type == "Output (PRINT V)":
            var = simpledialog.askstring("Input", "Enter variable:", parent=self)
            block = OutputBlock(block_id, event.x, event.y, var)
        elif "Condition" in block_type:
            var = simpledialog.askstring("Input", "Enter variable:", parent=self)
            value = simpledialog.askstring("Input", "Enter value:", parent=self)
            condition = "==" if "==" in block_type else "<"
            block = ConditionBlock(block_id, event.x, event.y, var, value, condition)
        else:
            return

        self.diagram.add_block(block)
        self.diagram.render(self)

    def on_block_click(self, event):
        """Обробляє клік на блок для початку перетягування"""
        item = self.find_closest(event.x, event.y)  # Знаходимо найближчий елемент
        for block in self.diagram.blocks:
            if block.rect_id == item[0]:  # Перевіряємо, чи це прямокутник блоку
                self.current_block = block
                self.offset_x = event.x - block.x
                self.offset_y = event.y - block.y
                break

    def on_block_drag(self, event):
        """Обробляє переміщення блоку"""
        if self.current_block is not None:
            # Нові координати блоку
            new_x = event.x - self.offset_x
            new_y = event.y - self.offset_y

            # Рух прямокутника і тексту
            dx = new_x - self.current_block.x
            dy = new_y - self.current_block.y
            self.move(self.current_block.rect_id, dx, dy)
            self.move(self.current_block.text_id, dx, dy)

            # Оновлення координат блоку
            self.current_block.x = new_x
            self.current_block.y = new_y

    def on_block_release(self, event):
        """Завершення перетягування блоку"""
        self.current_block = None

import tkinter as tk
from .block_options import BlockOptionsDialog
from .blocks import AssignmentBlock, ConstantBlock, InputBlock, OutputBlock, ConditionBlock
from .diagram import Diagram

class DiagramEditor(tk.Canvas):
    def __init__(self, parent, shared_variables):
        super().__init__(parent, bg="white", width=600, height=400)
        self.pack(fill=tk.BOTH, expand=True)
        self.shared_variables = shared_variables
        self.diagram = Diagram()

        self.current_block = None  # Поточний блок, який перетягують
        self.offset_x = 0  # Зміщення миші по X
        self.offset_y = 0  # Зміщення миші по Y

        self.bind("<Double-1>", self.add_block)  # Подвійний клік для додавання блоку
        self.bind("<Button-1>", self.on_block_click)  # Натискання для вибору блоку
        self.bind("<Button-3>", self.show_context_menu)  # Контекстне меню
        self.bind("<B1-Motion>", self.on_block_drag)  # Перетягування блоку
        self.bind("<ButtonRelease-1>", self.on_block_release)  # Завершення перетягування

        # Контекстне меню
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Видалити", command=self.delete_block)

    def add_block(self, event):
        """Додає блок з вибором типу після кліку"""
        block_id = len(self.diagram.blocks) + 1
        dialog = BlockOptionsDialog(self, title="Select Block Type")
        block_type = dialog.selected_option
        if block_type is None:
            return

        try:
            if block_type == "Assignment (V1 = V2)":
                block = AssignmentBlock(block_id, event.x, event.y, self.shared_variables, self)
            elif block_type == "Constant (V = C)":
                block = ConstantBlock(block_id, event.x, event.y, self.shared_variables, self)
            elif block_type == "Input (INPUT V)":
                block = InputBlock(block_id, event.x, event.y, self.shared_variables, self)
            elif block_type == "Output (PRINT V)":
                block = OutputBlock(block_id, event.x, event.y, self.shared_variables, self)
            elif block_type == "Condition (V == C)":
                block = ConditionBlock(block_id, event.x, event.y, self.shared_variables, self, "==")
            elif block_type == "Condition (V < C)":
                block = ConditionBlock(block_id, event.x, event.y, self.shared_variables, self, "<")
            else:
                return
        except ValueError:
            return  # Якщо вибір змінної чи значення було скасовано, блок не додається

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

    def show_context_menu(self, event):
        """Показати контекстне меню біля блоку"""
        item = self.find_closest(event.x, event.y)  # Знайти найближчий елемент
        for block in self.diagram.blocks:
            if block.rect_id == item[0]:  # Перевіряємо, чи це блок
                self.current_block = block
                # Отримуємо поточний колір та зберігаємо його
                original_fill = self.itemcget(block.rect_id, "fill")
                # Робимо блок затемненим
                self.itemconfig(block.rect_id, fill="gray")
                self.context_menu.post(event.x_root, event.y_root)
                # Повертаємо оригінальний колір
                self.itemconfig(block.rect_id, fill=original_fill)
                return

    def delete_block(self):
        """Видалити вибраний блок"""
        if self.current_block:
            # Видалення графічного представлення з Canvas
            self.delete(self.current_block.rect_id)
            self.delete(self.current_block.text_id)
            # Видалення блоку зі списку
            self.diagram.blocks.remove(self.current_block)
            self.current_block = None
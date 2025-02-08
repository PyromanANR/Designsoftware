import tkinter as tk
from .block_options import BlockOptionsDialog


class DiagramEditor(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="white", width=600, height=400)
        self.pack(fill=tk.BOTH, expand=True)

        self.blocks = []  # Список блоків
        self.current_block = None  # Поточний блок, який перетягують
        self.offset_x = 0  # Зміщення миші по X
        self.offset_y = 0  # Зміщення миші по Y

        self.bind("<Double-1>", self.add_block)  # Подвійний клік для додавання блоку
        self.bind("<Button-1>", self.on_block_click)  # Натискання для вибору блоку
        self.bind("<B1-Motion>", self.on_block_drag)  # Перетягування блоку
        self.bind("<ButtonRelease-1>", self.on_block_release)  # Завершення перетягування

    def add_block(self, event):
        """Додає блок з вибором типу після кліку"""
        dialog = BlockOptionsDialog(self, title="Select Block Type")
        block_type = dialog.selected_option
        if block_type is None:  # Якщо користувач закрив діалогове вікно
            return

        block_id = len(self.blocks) + 1
        x, y = event.x, event.y
        rect_id = self.create_rectangle(x, y, x + 200, y + 50, fill="lightblue", tags=f"block_{block_id}")
        text_id = self.create_text(x + 100, y + 25, text=f"{block_type} (Block {block_id})", tags=f"block_{block_id}")

        block = {
            "id": block_id,
            "x": x,
            "y": y,
            "type": block_type,
            "rect_id": rect_id,
            "text_id": text_id,
        }
        self.blocks.append(block)

    def on_block_click(self, event):
        """Обробляє клік на блок для початку перетягування"""
        item = self.find_closest(event.x, event.y)  # Знаходимо найближчий елемент
        for block in self.blocks:
            if block["rect_id"] == item[0]:  # Перевіряємо, чи це прямокутник блоку
                self.current_block = block
                self.offset_x = event.x - block["x"]
                self.offset_y = event.y - block["y"]
                break

    def on_block_drag(self, event):
        """Обробляє переміщення блоку"""
        if self.current_block is not None:
            # Нові координати блоку
            new_x = event.x - self.offset_x
            new_y = event.y - self.offset_y

            # Рух прямокутника і тексту
            dx = new_x - self.current_block["x"]
            dy = new_y - self.current_block["y"]
            self.move(self.current_block["rect_id"], dx, dy)
            self.move(self.current_block["text_id"], dx, dy)

            # Оновлення координат блоку
            self.current_block["x"] = new_x
            self.current_block["y"] = new_y

    def on_block_release(self, event):
        """Завершення перетягування блоку"""
        self.current_block = None

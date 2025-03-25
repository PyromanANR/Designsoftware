import tkinter as tk
from tkinter import ttk, messagebox
from .block_options import BlockOptionsDialog
from .blocks.AssignmentBlock import AssignmentBlock
from .blocks.ConstantBlock import ConstantBlock
from .blocks.InputBlock import InputBlock
from .blocks.OutputBlock import PrintBlock
from .blocks.ConditionBlock import ConditionBlock
from .blocks.EndBlock import EndBlock
from .blocks.StartBlock import StartBlock
from .diagram import Diagram

class DiagramEditor(tk.Canvas):
    def __init__(self, parent, shared_variables, diagram_name):
        super().__init__(parent, bg="white", width=600, height=400)
        self.pack(fill=tk.BOTH, expand=True)
        self.shared_variables = shared_variables
        self.diagram = Diagram(diagram_name, shared_variables)
        self.selected_block_for_link = None  # Блок для з'єднання

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
        self.context_menu.add_command(label="З'єднати", command=self.connect_blocks_dialog)



    def add_block(self, event):
        """Додає блок з вибором типу після кліку"""
        block_id = len(self.diagram.blocks) + 1
        dialog = BlockOptionsDialog(self, title="Виберіть тип блоку")
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
                block = PrintBlock(block_id, event.x, event.y, self.shared_variables, self)
            elif block_type == "Condition (V == C)":
                block = ConditionBlock(block_id, event.x, event.y, self.shared_variables, self, "==")
            elif block_type == "Condition (V < C)":
                block = ConditionBlock(block_id, event.x, event.y, self.shared_variables, self, "<")
            elif block_type == "End":
                block = EndBlock(block_id, event.x, event.y, self.shared_variables, self)
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
            if block.shape_id == item[0]:  # Перевіряємо, чи це прямокутник блоку
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
            self.move(self.current_block.shape_id, dx, dy)
            self.move(self.current_block.text_id, dx, dy)

            # Оновлення координат блоку
            self.current_block.x = new_x
            self.current_block.y = new_y

            self.redraw_connections()  # оновлення стрілок

    def on_block_release(self, event):
        """Завершення перетягування блоку"""
        self.current_block = None

    def show_context_menu(self, event):
        """Показати контекстне меню біля блоку"""
        item = self.find_closest(event.x, event.y)  # Знайти найближчий елемент
        for block in self.diagram.blocks:
            if block.shape_id == item[0]:  # Перевіряємо, чи це блок
                self.current_block = block
                # Отримуємо поточний колір та зберігаємо його
                original_fill = self.itemcget(block.shape_id, "fill")
                # Робимо блок затемненим
                self.itemconfig(block.shape_id, fill="gray")
                self.context_menu.post(event.x_root, event.y_root)
                # Повертаємо оригінальний колір
                self.itemconfig(block.shape_id, fill=original_fill)
                return

    def delete_block(self):
        """Видалити вибраний блок"""
        if self.current_block:
            # Видалення графічного представлення з Canvas
            self.delete(self.current_block.shape_id)
            self.delete(self.current_block.text_id)
            # Видалення блоку зі списку
            self.diagram.blocks.remove(self.current_block)
            self.current_block = None

    def connect_blocks_dialog(self):
        """Відкриває діалогове вікно з випадаючими списками для вибору блоків."""
        if self.current_block is None:
            return

        if isinstance(self.current_block, EndBlock):
            messagebox.showwarning("Помилка", "Блок 'Кінець' не може мати наступних блоків.")
            return

        available_blocks = [b for b in self.diagram.blocks if b != self.current_block and not isinstance(b, StartBlock)]
        if not available_blocks:
            messagebox.showwarning("Помилка", "Немає доступних блоків для з'єднання.")
            return

        dialog = tk.Toplevel(self)
        dialog.title("Вибір блоку для з'єднання")
        dialog.geometry("300x200")

        if isinstance(self.current_block, ConditionBlock):
            # Для блоків if – два випадаючі списки
            tk.Label(dialog, text="Оберіть блок для 'Так':").pack(pady=5)
            block_yes_var = tk.StringVar()
            block_yes_dropdown = ttk.Combobox(dialog, textvariable=block_yes_var, state="readonly",
                                              values=[b.text for b in available_blocks])
            block_yes_dropdown.pack(pady=5)

            tk.Label(dialog, text="Оберіть блок для 'Ні':").pack(pady=5)
            block_no_var = tk.StringVar()
            block_no_dropdown = ttk.Combobox(dialog, textvariable=block_no_var, state="readonly",
                                             values=[b.text for b in available_blocks])
            block_no_dropdown.pack(pady=5)

        else:
            # Для всіх інших блоків – один випадаючий список
            tk.Label(dialog, text="Оберіть блок для з'єднання:").pack(pady=5)
            block_var = tk.StringVar()
            block_dropdown = ttk.Combobox(dialog, textvariable=block_var, state="readonly",
                                          values=[b.text for b in available_blocks])
            block_dropdown.pack(pady=5)

        def confirm_connection():
            """Обробляє підтвердження вибору блоку для з'єднання."""
            if isinstance(self.current_block, ConditionBlock):
                block_yes = next((b for b in available_blocks if b.text == block_yes_var.get()), None)
                block_no = next((b for b in available_blocks if b.text == block_no_var.get()), None)

                if not block_yes or not block_no or block_yes == block_no:
                    messagebox.showwarning("Помилка", "Для умовного блоку потрібно вибрати два різні блоки.")
                    return

                self.current_block.add_next_block(block_yes, "так")
                self.current_block.add_next_block(block_no, "ні")

                # ✅ Змінюємо колір блоку для "так" на зелений
                self.itemconfig(block_yes.shape_id, fill="lightgreen")
                # ❌ Змінюємо колір блоку для "ні" на червоний
                self.itemconfig(block_no.shape_id, fill="lightcoral")

            else:
                selected_block = next((b for b in available_blocks if b.text == block_var.get()), None)
                if selected_block:
                    self.current_block.add_next_block(selected_block)

            self.redraw_connections()
            dialog.destroy()

        tk.Button(dialog, text="З'єднати", command=confirm_connection).pack(pady=10)

    def redraw_connections(self):
        """Перемальовує всі зв’язки між блоками."""
        self.delete("connection")
        for block in self.diagram.blocks:
            for next_block in block.next_blocks:
                if isinstance(next_block, tuple):  # Якщо це умовний зв'язок
                    target_block, _ = next_block
                else:
                    target_block = next_block

                self.create_line(block.x + 100, block.y + 50,
                                 target_block.x + 100, target_block.y,
                                 arrow=tk.LAST, tags="connection")

        # Оновлюємо кольори всіх блоків після перерисування
        for block in self.diagram.blocks:
            if isinstance(block, ConditionBlock):
                for next_block in block.next_blocks:
                    if isinstance(next_block, tuple):  # Для умовних блоків
                        target_block, condition = next_block
                        if condition == "так":
                            self.itemconfig(target_block.shape_id, fill="lightgreen")
                        elif condition == "ні":
                            self.itemconfig(target_block.shape_id, fill="lightcoral")
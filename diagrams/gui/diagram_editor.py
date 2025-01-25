import tkinter as tk

class DiagramEditor(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, bg="white", width=600, height=400)
        self.pack(fill=tk.BOTH, expand=True)
        self.blocks = []
        self.bind("<Button-1>", self.add_block)

    def add_block(self, event):
        """Додає блок на місце кліку"""
        block_id = len(self.blocks) + 1
        x, y = event.x, event.y
        block = {
            "id": block_id,
            "x": x,
            "y": y,
            "text": f"Block {block_id}"
        }
        self.blocks.append(block)
        self.create_rectangle(x, y, x + 100, y + 50, fill="lightblue")
        self.create_text(x + 50, y + 25, text=f"Block {block_id}")

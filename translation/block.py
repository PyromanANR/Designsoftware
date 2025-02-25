from abc import ABC, abstractmethod

class Block(ABC):
    """Базовий клас для всіх блоків"""

    def __init__(self, block_id):
        self.block_id = block_id

    @abstractmethod
    def generate_code(self):
        """Генерує код на Python"""
        pass
from translation.graph import Graph

class Thread:
    """Клас, що представляє один потік виконання."""

    def __init__(self, thread_id, shared_vars):
        self.thread_id = thread_id
        self.graph = Graph()
        self.shared_vars = shared_vars

    def build_from_json(self, thread_data):
        """Створює граф із JSON."""
        self.graph.build_from_json(thread_data)

    def get_code(self):
        """Отримує код для потоку."""
        return self.graph.generate_code()

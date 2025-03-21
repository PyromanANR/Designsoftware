import json
from factory import BlockFactory
from graph import Graph

class SharedVariables:
    """Клас для збереження та обробки спільних змінних."""
    def __init__(self, variables):
        self.variables = variables
    
    @classmethod
    def from_json(cls, json_data):
        return cls(json_data.get("shared_variables", {}))
    
    def __repr__(self):
        return str(self.variables)

class JSONParser:
    """Клас для обробки JSON-файлів та створення графа."""
    
    @staticmethod
    def parse_json(filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        graph = Graph()
        graph.build_from_json(data)
        shared_vars = SharedVariables.from_json(data)
        
        return graph, shared_vars
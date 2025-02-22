import os
import json

class TestManager:
    """
    Відповідає за пошук JSON-файлів із тестами в папці testing/test,
    завантаження тестів, зберігання в пам'яті.
    """
    def __init__(self, test_folder: str = None):
        # Можемо використати папку testing/test за замовчуванням
        self.test_folder = test_folder or os.path.join(os.getcwd(), "testing", "test")
        self._tests = []

    def find_existing_tests(self):
        """Повертає список шляхів до JSON-файлів, знайдених у test_folder."""
        if not os.path.isdir(self.test_folder):
            return []

        json_files = []
        for fname in os.listdir(self.test_folder):
            if fname.endswith(".json"):
                json_files.append(os.path.join(self.test_folder, fname))
        return json_files

    def load_tests_from_json(self, file_path: str):
        """Завантажує тести з JSON-файлу у внутрішній список _tests."""
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Перевіримо, чи data - список
        if not isinstance(data, list):
            raise ValueError("JSON root should be a list of test cases.")

        self._tests = data

    def tests_loaded(self) -> bool:
        """Перевіряє, чи є у менеджері хоч один тест."""
        return len(self._tests) > 0

    def get_tests(self):
        """Повертає список тестів."""
        return self._tests

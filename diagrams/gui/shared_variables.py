class SharedVariables:
    def __init__(self, update_callback):
        self.variables = {}  # {ім'я змінної: значення}
        self.update_callback = update_callback  # Викликається після змін

    def add_variable(self, name, value=0):
        if len(self.variables) >= 100 or name in self.variables:
            return False
        self.variables[name] = value
        self.update_callback()  # Оновлення GUI
        return True

    def remove_variable(self, name):
        """Видалення змінної + оновлення GUI"""
        if name in self.variables:
            del self.variables[name]
            self.update_callback()  # Оновлення GUI
            return True
        return False

    def update_variable(self, name, new_value):
        """Оновлення значення змінної + оновлення GUI"""
        if name in self.variables:
            self.variables[name] = new_value
            self.update_callback()  # Оновлення GUI
            return True
        return False

    def get_variables(self):
        return self.variables



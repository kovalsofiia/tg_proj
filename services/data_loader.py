import json

class DataLoader:
    def __init__(self, file_path: str = "data_uk.json"):
        self.data = self.load_data(file_path)

    def load_data(self, file_path: str) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Помилка: Файл data_uk.json не знайдено.")
            return {}
        except json.JSONDecodeError:
            print("Помилка: Некоректний формат data_uk.json.")
            return {}

    def get_roles(self) -> list:
        return self.data.get('roles', [])

    def get_faculties(self) -> list:
        return self.data.get('faculties', [])

    def get_departments(self, faculty: str) -> list:
        return self.data.get('departments', {}).get(faculty, [])

    def get_education_degrees(self) -> list:
        return self.data.get('degrees', [])

    def get_ui_text(self) -> dict:
        return self.data.get('ui_text', {})
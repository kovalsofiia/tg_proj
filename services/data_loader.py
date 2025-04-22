import json

class DataLoader:
    def __init__(self, file_path='data_uk.json'):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Помилка: Файл {self.file_path} не знайдено.")
            return {}

    def get_ui_text(self):
        return self.data.get('ui_text', {})

    def get_roles(self):
        return self.data.get('roles', [])

    def get_faculties(self):
        return self.data.get('faculties', [])

    def get_departments(self, faculty):
        return self.data.get('departments', {}).get(faculty, [])
    
    def get_education_degrees(self):
        return self.data.get('degrees', [])
    
    def get_positions(self):
        return self.data.get('positions', [])

    def get_documents(self, role):
        return self.data.get('documents', {}).get(role, [])

    def get_popular_documents(self, role):
        return self.data.get('popular_documents', {}).get(role, [])

    def get_document_fields(self, document):
        return self.data.get('document_fields', {}).get(document, [])
    
    def get_document_template(self, document):
        return self.data.get('document_templates', {}).get(document, {})
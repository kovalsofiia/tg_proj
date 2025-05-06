from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class UIBuilder:
    def __init__(self, ui_text):
        self.ui_text = ui_text

    def build_selection_text(self, user_data):
        selection = ""
        role = user_data.get('role')
        
        if role:
            selection += f"{self.ui_text.get('role_label', 'Роль')}: {role}\n"
        if 'faculty' in user_data and user_data['faculty'] is not None:
            selection += f"{self.ui_text.get('faculty_label', 'Факультет')}: {user_data['faculty']}\n"
        
        # Для студентів відображаємо спеціальність, для працівників — кафедру
        if role == "Студент":
            if 'speciality' in user_data and user_data['speciality'] is not None:
                selection += f"{self.ui_text.get('speciality_label', 'Спеціальність')}: {user_data['speciality']}\n"
            if 'education_degree' in user_data and user_data['education_degree'] is not None:
                selection += f"{self.ui_text.get('education_degree_label', 'Освітній ступінь')}: {user_data['education_degree']}\n"
            if 'course' in user_data and user_data['course'] is not None:
                selection += f"{self.ui_text.get('course_label', 'Курс')}: {user_data['course']}\n"
        else:  # Працівник університету
            if 'department' in user_data and user_data['department'] is not None:
                selection += f"{self.ui_text.get('department_label', 'Кафедра')}: {user_data['department']}\n"
            if 'position' in user_data and user_data['position'] is not None:
                selection += f"{self.ui_text.get('position_label', 'Посада')}: {user_data['position']}\n"
        
        if 'document' in user_data and user_data['document'] is not None:
            selection += f"{self.ui_text.get('document_label', 'Документ')}: {user_data['document']}\n"
        return selection

    def build_keyboard(self, items, callback_prefix):
        keyboard = []
        for item in items:
            if isinstance(item, tuple):
                # Якщо item є кортежем (key, name), використовуємо key для callback_data, name для тексту кнопки
                key, name = item
                button = InlineKeyboardButton(name, callback_data=f'{callback_prefix}{key}')
            else:
                # Якщо item є рядком, використовуємо його для обох
                button = InlineKeyboardButton(item, callback_data=f'{callback_prefix}{item}')
            keyboard.append([button])
        return InlineKeyboardMarkup(keyboard)

    def build_confirmation_text(self, user_data, output_format='docx'):
        document = user_data.get('document')
        if not document:
            return "Помилка: документ не обрано."

        # Отримуємо всі поля для документа
        document_fields = self.ui_text.get('document_fields', {}).get(document, [])
        field_labels = {field['name']: field['label'] for field in document_fields}

        confirmation_text = f"{self.ui_text.get('confirm_data', 'Будь ласка, перевірте введені дані:')}\n\n"
        confirmation_text += "📋 Основні дані:\n"
        
        # Основні поля (role, faculty, full_name тощо)
        for key, value in user_data.items():
            if key == 'additional_data' or key is None or value is None:
                continue
            label = field_labels.get(key, self.ui_text.get(f'{key}_label', key.replace('_', ' ').title()))
            confirmation_text += f"  • {label}: {value}\n"

        # Додаткові дані
        additional_data = user_data.get('additional_data', {})
        if additional_data:
            confirmation_text += "\n📎 Додаткові дані:\n"
            for key, value in additional_data.items():
                if key is None or value is None:
                    continue
                label = field_labels.get(key, key.replace('_', ' ').title())
                confirmation_text += f"  • {label}: {value}\n"

        confirmation_text += f"\n📄 Обраний формат: {output_format.upper()}"
        return confirmation_text

    def build_confirmation_keyboard(self, output_format):
        keyboard = [
            [InlineKeyboardButton("✅ DOCX" if output_format == 'docx' else "DOCX", callback_data='format_docx'),
             InlineKeyboardButton("✅ PDF" if output_format == 'pdf' else "PDF", callback_data='format_pdf')],
            [InlineKeyboardButton(self.ui_text.get('confirm_button'), callback_data='confirm')],
            [InlineKeyboardButton(self.ui_text.get('change_button'), callback_data='change')],
        ]
        return InlineKeyboardMarkup(keyboard)

    def build_all_documents_keyboard(self, documents):
        keyboard = [[InlineKeyboardButton(doc, callback_data=f'doc_id_{i}')] for i, doc in enumerate(documents)]
        return InlineKeyboardMarkup(keyboard)
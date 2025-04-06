from telegram import InlineKeyboardButton, InlineKeyboardMarkup

class UIBuilder:
    def __init__(self, ui_text):
        self.ui_text = ui_text

    def build_selection_text(self, user_data):
        selection = ""
        if 'role' in user_data:
            selection += f"{self.ui_text.get('role_label', 'Роль')}: {user_data['role']}\n"
        if 'faculty' in user_data:
            selection += f"{self.ui_text.get('faculty_label', 'Факультет')}: {user_data['faculty']}\n"
        if 'department' in user_data:
            selection += f"{self.ui_text.get('department_label', 'Кафедра')}: {user_data['department']}\n"
        if 'education_degree' in user_data:
            selection += f"{self.ui_text.get('education_degree_label', 'Освітній ступінь')}: {user_data['education_degree']}\n"
        if 'speciality' in user_data:
            selection += f"{self.ui_text.get('speciality_label', 'Спеціальність')}: {user_data['speciality']}\n"
        if 'course' in user_data:
            selection += f"{self.ui_text.get('course_label', 'Курс')}: {user_data['course']}\n"
        if 'position' in user_data:
            selection += f"{self.ui_text.get('position_label', 'Посада')}: {user_data['position']}\n"
        if 'document' in user_data:
            selection += f"{self.ui_text.get('document_label', 'Документ')}: {user_data['document']}\n"
        return selection

    def build_keyboard(self, items, callback_prefix):
        keyboard = [[InlineKeyboardButton(item, callback_data=f'{callback_prefix}{item}')] for item in items]
        return InlineKeyboardMarkup(keyboard)

    def build_confirmation_text(self, user_data, output_format='docx'):
        confirmation_text = self.ui_text.get('confirm_data') + "\n\n"
        for key, value in user_data.items():
            if key not in ['role', 'faculty', 'department', 'document', 'education_degree', 'speciality', 'course', 'position']:
                confirmation_text += f"{key.replace('_', ' ').title()}: {value}\n"
            elif key in ['faculty', 'department', 'role', 'document', 'education_degree', 'speciality', 'course', 'position']:
                confirmation_text += f"{self.ui_text.get(f'{key}_label', key.title())}: {value}\n"
        if 'additional_data' in user_data:
            confirmation_text += f"\n{self.ui_text.get('additional_data_label', 'Додаткові дані')}:\n"
            for key, value in user_data['additional_data'].items():
                confirmation_text += f"- {key.replace('_', ' ').title()}: {value}\n"
        confirmation_text += f"\nОбраний формат: {output_format.upper()}"
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
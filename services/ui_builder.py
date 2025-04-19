from telegram import InlineKeyboardMarkup
from utils.keyboards import build_inline_keyboard

class UIBuilder:
    def build_keyboard(self, items: list, prefix: str) -> InlineKeyboardMarkup:
        return build_inline_keyboard(items, prefix)

    def build_selection_text(self, user_data: dict) -> str:
        selection = ""
        if 'role' in user_data:
            selection += f"Роль: {user_data['role']}\n"
        if 'full_name' in user_data:
            selection += f"ПІБ: {user_data['full_name']}\n"
        if 'phone_number' in user_data:
            selection += f"Номер телефону: {user_data['phone_number']}\n"
        if 'faculty' in user_data:
            selection += f"Факультет: {user_data['faculty']}\n"
        if 'education_degree' in user_data:
            selection += f"Освітній ступінь: {user_data['education_degree']}\n"
        if 'department' in user_data:
            selection += f"Кафедра: {user_data['department']}\n"
        return selection
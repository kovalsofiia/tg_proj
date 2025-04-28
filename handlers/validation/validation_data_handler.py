import re
from datetime import datetime

def determine_field_type(field_name: str) -> str:
    """Визначає тип поля на основі його назви."""
    field_name = field_name.lower()
    if 'date' in field_name:
        return 'date'
    elif 'course' in field_name:
        return 'number'
    elif 'phone' in field_name:
        return 'phone'
    elif 'subject' in field_name:
        return 'subject'
    return 'text'  # За замовчуванням вважаємо текстом

def validate_date(date_text: str, field_name: str) -> tuple[bool, str]:
    """Перевіряє формат дати DD.MM.YYYY та чи є дата коректною."""
    pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    if not re.match(pattern, date_text):
        return False, "invalid_date_format"

    try:
        date = datetime.strptime(date_text, '%d.%m.%Y')
        current_date = datetime.now()

        if date.year > current_date.year + 5:
            return False, "date_too_far"

        if 'end_date' in field_name.lower():
            current_date_only = current_date.date()
            date_only = date.date()
            if date_only < current_date_only:
                return False, "end_date_in_past"

        return True, ""
    except ValueError:
        return False, "invalid_date"

def validate_text(text: str, min_length: int = 1) -> tuple[bool, str]:
    """Перевіряє, чи текст не порожній і має достатню довжину."""
    if not text or len(text.strip()) < min_length:
        return False, "text_too_short"
    return True, ""

def validate_subject(subject: str) -> tuple[bool, str]:
    """Перевіряє, чи назва предмета є коректним текстом."""
    pattern = r'^[a-zA-Zа-яА-Я\s\-]+$'
    if not re.match(pattern, subject):
        return False, "invalid_subject_format"
    if len(subject.strip()) < 3:
        return False, "subject_too_short"
    return True, ""
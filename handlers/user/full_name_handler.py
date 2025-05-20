from telegram.ext import CallbackContext
from telegram import Update
from config import FULL_NAME, PHONE_NUMBER, FULL_NAME_REGEX
import re
from services.keyboards import get_phone_keyboard
from services.data_storage import DataStorage

# Функція визначення статі за по батькові
def detect_gender_by_patronymic(full_name: str) -> str:
    parts = full_name.strip().split()
    if len(parts) >= 3:
        patronymic = parts[2]
        if re.fullmatch(r"[А-ЯІЇЄ][а-яіїєґ']*(ович|йович)", patronymic):
            return "Студента"
        elif re.fullmatch(r"[А-ЯІЇЄ][а-яіїєґ']*(івна|ївна)", patronymic):
            return "Студентки"
    return "unknown"

async def get_full_name(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    user_id = update.effective_user.id
    full_name = update.message.text

    if re.match(FULL_NAME_REGEX, full_name):
        # Створюємо скорочене ПІБ
        def create_short_name(full_name):
            parts = full_name.split()
            if len(parts) >= 3:
                surname, first_name, patronymic = parts[:3]
                return f"{surname} {first_name[0]}.{patronymic[0]}."
            elif len(parts) == 2:
                surname, first_name = parts
                return f"{surname} {first_name[0]}."
            return full_name  # Якщо ПІБ нестандартне, повертаємо як є

        short_name = create_short_name(full_name)
        

        # 🔹 Визначення статі для студента
        gender = detect_gender_by_patronymic(full_name)
        # Зберігаємо обидва поля
        user_data_store.set_user_data(user_id, 'full_name', full_name)
        user_data_store.set_user_data(user_id, 'short_name', short_name)
        user_data_store.set_user_data(user_id, 'gender', gender)
        
        reply_markup = get_phone_keyboard()
        await update.message.reply_text("Будь ласка, поділіться своїм номером телефону, натиснувши кнопку:", reply_markup=reply_markup)
        return PHONE_NUMBER
    else:
        await update.message.reply_text(data_loader.get_ui_text().get('incorrect_full_name'))
        return FULL_NAME

async def full_name_received(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    return await get_full_name(update, context, data_loader, ui_builder, user_data_store)
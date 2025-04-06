from telegram.ext import CallbackContext
from telegram import Update
from config import FULL_NAME, PHONE_NUMBER, FULL_NAME_REGEX
import re
from utils.keyboards import get_phone_keyboard

async def get_full_name(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> int:
    user_id = update.effective_user.id
    full_name = update.message.text

    if re.match(FULL_NAME_REGEX, full_name):
        user_data_store[user_id]['full_name'] = full_name  # Зберігаємо ПІБ безпосередньо
        reply_markup = get_phone_keyboard()
        await update.message.reply_text("Будь ласка, поділіться своїм номером телефону, натиснувши кнопку:", reply_markup=reply_markup)
        return PHONE_NUMBER
    else:
        await update.message.reply_text(data_loader.get_ui_text().get('incorrect_full_name'))
        return FULL_NAME

async def full_name_received(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> int:
    # Цей обробник тепер викликається після вибору ролі "Студент"
    return await get_full_name(update, context, data_loader, ui_builder, user_data_store)
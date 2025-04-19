# ADDED JSON SAVING easy alternative for saving data
from telegram.ext import CallbackContext
from telegram import Update
from config import FACULTY, PHONE_NUMBER
from utils.keyboards import get_phone_keyboard
from utils.data_storage import DataStorage
import re

PHONE_REGEX = r'^\+?\d{10,15}$'

async def get_phone_number(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    user_id = update.effective_user.id
    contact = update.message.contact
    phone_number = None

    if contact:
        phone_number = contact.phone_number
    elif update.message.text:
        phone_number = update.message.text.strip()
        if not re.match(PHONE_REGEX, phone_number):
            await update.message.reply_text("Некоректний формат номера телефону. Введіть номер у форматі +380123456789 або скористайтеся кнопкою:", reply_markup=get_phone_keyboard())
            return PHONE_NUMBER

    if phone_number:
        user_data_store.set_user_data(user_id, 'phone_number', phone_number)
        faculties = data_loader.get_faculties()
        reply_markup = ui_builder.build_keyboard(faculties, 'faculty_')
        current_selection = ui_builder.build_selection_text(user_data_store.get_user_data(user_id))
        message_text = f"{current_selection}\nБудь ласка, оберіть ваш факультет:"
        await update.message.reply_text(text=message_text, reply_markup=reply_markup)
        return FACULTY
    else:
        reply_markup = get_phone_keyboard()
        await update.message.reply_text("Будь ласка, скористайтеся кнопкою, щоб поділитися номером телефону:", reply_markup=reply_markup)
        return PHONE_NUMBER

async def phone_number_received(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    return await get_phone_number(update, context, data_loader, ui_builder, user_data_store)
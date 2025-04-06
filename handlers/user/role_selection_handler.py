from telegram.ext import CallbackContext
from telegram import Update
from config import FULL_NAME

async def role_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    role = query.data.split('_')[1]
    user_data_store[user_id]['role'] = role

    await query.edit_message_text(
        text="Будь ласка, введіть ваше Прізвище, Ім'я та По-батькові повністю:"
    )
    return FULL_NAME
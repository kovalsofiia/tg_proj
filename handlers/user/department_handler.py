from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from config import CONFIRMATION
from utils.data_storage import DataStorage

async def department_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    department = query.data.split('_')[1]
    
    user_data_store.set_user_data(user_id, 'department', department)
    
    current_selection = ui_builder.build_selection_text(user_data_store.get_user_data(user_id))
    message_text = f"{data_loader.get_ui_text().get('confirm_data')}\n\n{current_selection}"
    keyboard = [[InlineKeyboardButton(data_loader.get_ui_text().get('confirm_button'), callback_data='confirm')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=message_text, reply_markup=reply_markup)
    return CONFIRMATION
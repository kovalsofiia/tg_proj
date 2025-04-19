from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update
from utils.data_storage import DataStorage

async def confirm_data(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    user_data = user_data_store.get_user_data(user_id)
    
    await query.edit_message_text(
        text=f"Дякую за підтвердження!\n\nВведені дані:\n{ui_builder.build_selection_text(user_data)}"
    )
    user_data_store.clear_user_data(user_id)
    return ConversationHandler.END
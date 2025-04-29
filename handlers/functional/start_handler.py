from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update
from config import ROLE

async def start(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> int:
    user_id = update.effective_user.id
    user_data_store.clear_user_data(user_id)
    roles = data_loader.get_roles()
    if not roles:
        await update.message.reply_text("Помилка: список ролей недоступний. Спробуйте пізніше.")
        return ConversationHandler.END
    reply_markup = ui_builder.build_keyboard(roles, 'role_')
    await update.message.reply_text(data_loader.get_ui_text().get('start_message'), reply_markup=reply_markup)
    return ROLE
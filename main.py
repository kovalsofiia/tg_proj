# ADDED JSON SAVING easy alternative for saving data
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters, CallbackContext
from config import ROLE, FULL_NAME, PHONE_NUMBER, FACULTY, EDUCATION_DEGREE, DEPARTMENT, CONFIRMATION
from utils.data_storage import DataStorage
from services.data_loader import DataLoader
from services.ui_builder import UIBuilder
from handlers.user.role_selection_handler import role_chosen
from handlers.user.full_name_handler import full_name_received
from handlers.user.phone_number_handler import phone_number_received
from handlers.user.faculty_selection_handler import faculty_chosen
from handlers.user.education_degree_handler import education_degree_chosen
from handlers.user.department_handler import department_chosen
from handlers.user.confirmation_handler import confirm_data

load_dotenv()

async def start(update: Update, context: CallbackContext, data_loader: DataLoader, ui_builder: UIBuilder, user_data_store: DataStorage) -> int:
    user_id = update.effective_user.id
    user_data_store.clear_user_data(user_id)
    roles = data_loader.get_roles()
    reply_markup = ui_builder.build_keyboard(roles, 'role_')
    await update.message.reply_text(data_loader.get_ui_text().get('start_message'), reply_markup=reply_markup)
    return ROLE

async def cancel(update: Update, context: CallbackContext, data_loader: DataLoader, user_data_store: DataStorage) -> int:
    user = update.effective_user
    await update.message.reply_text(
        data_loader.get_ui_text().get('cancel_message').format(first_name=user.first_name)
    )
    user_data_store.clear_user_data(user.id)
    return ConversationHandler.END

def main() -> None:
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        print("Error: BOT_TOKEN not found in .env file.")
        return

    data_loader = DataLoader()
    ui_builder = UIBuilder()
    user_data_store = DataStorage()

    application = ApplicationBuilder().token(bot_token).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", lambda update, context: start(update, context, data_loader, ui_builder, user_data_store))],
        states={
            ROLE: [CallbackQueryHandler(lambda update, context: role_chosen(update, context, data_loader, ui_builder, user_data_store), pattern='^role_')],
            FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: full_name_received(update, context, data_loader, ui_builder, user_data_store))],
            PHONE_NUMBER: [MessageHandler(filters.CONTACT | filters.TEXT & ~filters.COMMAND, lambda update, context: phone_number_received(update, context, data_loader, ui_builder, user_data_store))],
            FACULTY: [CallbackQueryHandler(lambda update, context: faculty_chosen(update, context, data_loader, ui_builder, user_data_store), pattern='^faculty_')],
            EDUCATION_DEGREE: [CallbackQueryHandler(lambda update, context: education_degree_chosen(update, context, data_loader, ui_builder, user_data_store), pattern='^degree_')],
            DEPARTMENT: [CallbackQueryHandler(lambda update, context: department_chosen(update, context, data_loader, ui_builder, user_data_store), pattern='^department_')],
            CONFIRMATION: [CallbackQueryHandler(lambda update, context: confirm_data(update, context, data_loader, ui_builder, user_data_store), pattern='^confirm$')],
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: cancel(update, context, data_loader, user_data_store))],
        per_message=False
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()

import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from services.data_loader import DataLoader
from services.ui_builder import UIBuilder
from services.document_generator import DocumentGenerator
from utils.data_storage import DataStorage
from conversation import ConversationManager

def main() -> None:
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        print("Error: BOT_TOKEN not found in .env file.")
        return

    # Ініціалізація компонентів
    data_loader = DataLoader()
    ui_builder = UIBuilder(data_loader.get_ui_text())
    doc_generator = DocumentGenerator()  # Потрібно реалізувати
    user_data_store = DataStorage()

    # Налаштування бота
    application = ApplicationBuilder().token(bot_token).build()
    conversation_manager = ConversationManager(application, data_loader, ui_builder, doc_generator, user_data_store)
    conversation_manager.setup_handlers()

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()

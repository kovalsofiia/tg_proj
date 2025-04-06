from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN
from services.data_loader import DataLoader
from services.document_generator import DocumentGenerator
from services.ui_builder import UIBuilder
from conversation import ConversationManager

USER_DATA = {}

def main():
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN not found in .env file.")
        return

    data_loader = DataLoader()
    ui_builder = UIBuilder(data_loader.get_ui_text())
    doc_generator = DocumentGenerator()
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    conversation_manager = ConversationManager(application, data_loader, ui_builder, doc_generator, USER_DATA)
    conversation_manager.setup_handlers()

    application.run_polling()

if __name__ == '__main__':
    main()
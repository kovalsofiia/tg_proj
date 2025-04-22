from telegram.ext import CallbackContext
from telegram import Update
from config import ADDITIONAL_DATA, CONFIRMATION
from handlers.system.confirmation_handlers import display_confirmation
from utils.data_storage import DataStorage
from datetime import datetime
import re

# Список полів, які мають бути датами (на основі data_uk.json)
DATE_FIELDS = ['start_date', 'end_date', 'event_date', 'note_date', 'exam_date']

def validate_date(date_text: str) -> bool:
    """
    Перевіряє, чи відповідає введений текст формату дати DD.MM.YYYY.
    Повертає True, якщо формат правильний, інакше False.
    """
    # Регулярний вираз для формату DD.MM.YYYY
    pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    if not re.match(pattern, date_text):
        return False
    
    try:
        # Перевіряємо, чи є дата коректною
        datetime.strptime(date_text, '%d.%m.%Y')
        return True
    except ValueError:
        return False

async def prompt_for_field(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage, user_id: int, field: dict) -> None:
    """Prompt user for a specific field."""
    await update.message.reply_text(
        f"{ui_builder.build_selection_text(user_data_store.get_user_data(user_id))}\n{data_loader.get_ui_text().get('enter_your')} {field['label']}:"
    )

async def additional_data_received(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    user_id = update.effective_user.id
    field = context.user_data['fields_to_ask'][0]
    field_name = field['name']
    field_value = update.message.text
    user_data = user_data_store.get_user_data(user_id)

    # Валідація, якщо поле є датою
    if field_name in DATE_FIELDS:
        if not validate_date(field_value):
            # Якщо дата некоректна, повідомляємо користувача і просимо ввести ще раз
            await update.message.reply_text(data_loader.get_ui_text().get('invalid_date_format'))
            return ADDITIONAL_DATA  # Залишаємося в стані ADDITIONAL_DATA для повторного введення

    # Зберігаємо значення поля
    if 'additional_data' not in user_data:
        user_data_store.set_user_data(user_id, 'additional_data', {})
    additional_data = user_data_store.get_user_data(user_id).get('additional_data', {})
    additional_data[field_name] = field_value
    user_data_store.set_user_data(user_id, 'additional_data', additional_data)
    
    # Видаляємо оброблене поле зі списку
    context.user_data['fields_to_ask'].pop(0)
    
    # Перевіряємо, чи є ще поля для введення
    if context.user_data['fields_to_ask']:
        next_field = context.user_data['fields_to_ask'][0]
        await prompt_for_field(update, context, data_loader, ui_builder, user_data_store, user_id, next_field)
        return ADDITIONAL_DATA
    else:
        await display_confirmation(update, context, ui_builder, user_data_store)
        return CONFIRMATION

async def prepare_additional_fields(context: CallbackContext, document: str, data_loader, user_data_store: DataStorage, user_id: int) -> list:
    """Prepare list of fields to ask, excluding those already in user_data."""
    # Get all required fields for the document
    all_fields = data_loader.get_document_fields(document)
    
    # Get current user data
    user_data = user_data_store.get_user_data(user_id)
    
    # Initialize fields to ask
    fields_to_ask = []
    
    # Check each field and only add if not already present in user_data
    for field in all_fields:
        field_name = field["name"] if isinstance(field, dict) else field
        field_label = field["label"] if isinstance(field, dict) else field
        
        # Check if field exists in main user_data or additional_data
        if (field_name not in user_data and 
            (not user_data.get('additional_data') or field_name not in user_data.get('additional_data', {}))):
            fields_to_ask.append({"name": field_name, "label": field_label})
    
    return fields_to_ask
from telegram.ext import CallbackContext
from telegram import Update
from config import ADDITIONAL_DATA, CONFIRMATION
from handlers.functional.confirmation_handlers import display_confirmation
from handlers.validation.validation_data_handler import determine_field_type, validate_date, validate_subject, validate_text, validate_id_code, validate_card_number
from services.data_storage import DataStorage
from datetime import datetime
import re


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

    # Визначаємо тип поля автоматично за назвою
    field_type = determine_field_type(field_name)

    # Отримуємо параметри валідації з метаданих (якщо є)
    min_length = field.get('min_length', 5)  # За замовчуванням 5 для текстових полів

    # Отримуємо ui_text для перевірки наявності ключів
    ui_text = data_loader.get_ui_text()

    # 🔸 Відображення додаткового тексту з ui_text.json
    if (
        user_data.get('document') == "Заява на академ. відпустку" and 
        field_name.lower() == "reason"
    ):
        note_key = "academic_leave_reason_note"
        if note_key in ui_text:
            await update.message.reply_text(ui_text[note_key])

    # Валідація залежно від типу поля
    if field_type == 'date':
        is_valid, error_key = validate_date(field_value, field_name)
        if not is_valid:
            if error_key not in ui_text:
                await update.message.reply_text("Помилка валідації. Будь ласка, спробуйте ще раз.")
                return ADDITIONAL_DATA
            error_message = ui_text[error_key]
            await update.message.reply_text(error_message)
            return ADDITIONAL_DATA
    elif field_type == 'subject':
        is_valid, error_key = validate_subject(field_value)
        if not is_valid:
            if error_key not in ui_text:
                await update.message.reply_text("Помилка валідації. Будь ласка, спробуйте ще раз.")
                return ADDITIONAL_DATA
            error_message = ui_text[error_key]
            await update.message.reply_text(error_message)
            return ADDITIONAL_DATA
    
    elif field_type == 'id_code':
        is_valid, error_key = validate_id_code(field_value)
        if not is_valid:
            error_message = ui_text.get(error_key, "Невірний ідентифікаційний код.")
            await update.message.reply_text(error_message)
            return ADDITIONAL_DATA

    elif field_type == 'card_number':
        is_valid, error_key = validate_card_number(field_value)
        if not is_valid:
            error_message = ui_text.get(error_key, "Невірний номер карткового рахунку.")
            await update.message.reply_text(error_message)
            return ADDITIONAL_DATA

    else:  # Усі інші поля вважаємо текстовими
        is_valid, error_key = validate_text(field_value, min_length=min_length)
        if not is_valid:
            if error_key not in ui_text:
                await update.message.reply_text("Помилка валідації. Будь ласка, спробуйте ще раз.")
                return ADDITIONAL_DATA
            error_message = ui_text[error_key].format(min_length=min_length)
            await update.message.reply_text(error_message)
            return ADDITIONAL_DATA
        
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
    all_fields = data_loader.get_document_fields(document)
    user_data = user_data_store.get_user_data(user_id)
    fields_to_ask = []
    for field in all_fields:
        field_name = field["name"]
        field_label = field["label"]
        field_source = field.get("source", "user_data")
        if (field_source != "system" and 
            field_name not in user_data and 
            (not user_data.get('additional_data') or field_name not in user_data.get('additional_data', {}))):
            fields_to_ask.append({"name": field_name, "label": field_label})
    return fields_to_ask
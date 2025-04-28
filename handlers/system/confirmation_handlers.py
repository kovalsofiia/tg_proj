from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler
import os
from config import DOCUMENT, CONFIRMATION, REPEAT, EDIT_DATA
from handlers.validation.validation_data_handler import determine_field_type, validate_date, validate_text, validate_subject

async def display_confirmation(update: Update, context: CallbackContext, ui_builder, user_data_store) -> int:
    user_id = update.effective_user.id
    output_format = context.user_data.get('output_format', 'docx')
    confirmation_text = ui_builder.build_confirmation_text(user_data_store.get_user_data(user_id), output_format)
    reply_markup = ui_builder.build_confirmation_keyboard(output_format)
    if update.message:
        await update.message.reply_text(confirmation_text, reply_markup=reply_markup)
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(confirmation_text, reply_markup=reply_markup)
    return CONFIRMATION

async def format_chosen(update: Update, context: CallbackContext, ui_builder, user_data_store) -> int:
    query = update.callback_query
    await query.answer()
    format_choice = query.data.split('_')[1]
    context.user_data['output_format'] = format_choice
    user_id = update.effective_user.id
    confirmation_text = ui_builder.build_confirmation_text(user_data_store.get_user_data(user_id), format_choice)
    reply_markup = ui_builder.build_confirmation_keyboard(format_choice)
    await query.edit_message_text(confirmation_text, reply_markup=reply_markup)
    return CONFIRMATION

async def confirm_data(update: Update, context: CallbackContext, doc_generator, user_data_store) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    user_data = user_data_store.get_user_data(user_id)
    document_name = user_data.get('document', 'документ')
    output_format = context.user_data.get('output_format', 'docx')
    try:
        file_path = doc_generator.generate(user_data, output_format=output_format)
        await query.edit_message_text(f"Документ '{document_name}' успішно згенеровано!")
        with open(file_path, 'rb') as f:
            await context.bot.send_document(
                chat_id=user_id,
                document=f,
                filename=f"{document_name}.{output_format}"
            )
        os.remove(file_path)
    except Exception as e:
        await query.edit_message_text(f"Помилка при генерації документа: {str(e)}")
        return ConversationHandler.END

    # Запит на повторну генерацію
    keyboard = [
        [InlineKeyboardButton("Так", callback_data='repeat_yes')],
        [InlineKeyboardButton("Ні", callback_data='repeat_no')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=user_id, text="Бажаєте згенерувати ще один документ?", reply_markup=reply_markup)
    return REPEAT

async def repeat_choice(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    choice = query.data

    if choice == 'repeat_yes':
        # Отримати поточні дані користувача
        user_data = user_data_store.get_user_data(user_id)
        role = user_data.get('role')
        if not role:
            await query.edit_message_text("Помилка: роль не визначена. Почніть з /start.")
            return ConversationHandler.END

        # Зберегти базову інформацію
        base_data = {
            'role': role,
            'full_name': user_data.get('full_name'),
            'phone_number': user_data.get('phone_number'),
            'faculty': user_data.get('faculty')
        }
        if role == "Студент":
            base_data.update({
                'education_degree': user_data.get('education_degree'),
                'speciality': user_data.get('speciality'),
                'course': user_data.get('course')
            })
        elif role == "Працівник університету":
            base_data.update({
                'department': user_data.get('department'),
                'position': user_data.get('position')
            })

        user_data_store.set_user_data(user_id, 'document', None)
        user_data_store.set_user_data(user_id, 'additional_data', {})

        # Повертаємося до вибору документів
        popular_docs = data_loader.get_popular_documents(role)
        all_docs = data_loader.get_documents(role)
        keyboard = [[InlineKeyboardButton(doc, callback_data=f'document_{doc}')] for doc in popular_docs]
        if all_docs and popular_docs != all_docs:
            keyboard.append([InlineKeyboardButton(data_loader.get_ui_text().get('all_documents_button'), callback_data='show_all_documents')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Показати збережені дані та запит на вибір документа
        current_selection = ui_builder.build_selection_text(user_data_store.get_user_data(user_id))
        message_text = f"{current_selection}\n{data_loader.get_ui_text().get('choose_document')}\n{data_loader.get_ui_text().get('popular_documents')}"
        await query.edit_message_text(text=message_text, reply_markup=reply_markup)
        return DOCUMENT
    else:  # 'repeat_no'
        await query.edit_message_text("Дякую за використання бота! До зустрічі!")
        user_data_store.clear_user_data(user_id)
        return ConversationHandler.END

async def change_data(update: Update, context: CallbackContext, data_loader, user_data_store) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    user_data = user_data_store.get_user_data(user_id)
    additional_data = user_data.get('additional_data', {})

    fields = []
    for key, value in user_data.items():
        if key != 'additional_data' and value is not None and key is not None:
            fields.append((key, value))
    for key, value in additional_data.items():
        if key is not None and value is not None:
            fields.append((key, value))

    if not fields:
        await query.edit_message_text("Немає даних для редагування.")
        return CONFIRMATION

    keyboard = []
    for field_name, field_value in fields:
        keyboard.append([InlineKeyboardButton(f"{field_name}: {field_value}", callback_data=f"edit_{field_name}")])
    keyboard.append([InlineKeyboardButton("Назад", callback_data='back_to_confirm')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Оберіть поле для редагування:", reply_markup=reply_markup)
    return EDIT_DATA

async def edit_field_callback(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id

    if query.data == 'back_to_confirm':
        return await display_confirmation(update, context, ui_builder, user_data_store)

    field_name = query.data.replace("edit_", "")
    context.user_data['field_to_edit'] = field_name

    await query.edit_message_text(f"Введіть нове значення для {field_name}:")
    return EDIT_DATA

async def edit_field_received(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> int:
    user_id = update.effective_user.id
    field_name = context.user_data.get('field_to_edit')
    new_value = update.message.text
    ui_text = data_loader.get_ui_text() # Отримуємо ui_text для повідомлень

    # Переконуємося, що field_name не None
    if field_name is None:
        await update.message.reply_text("Помилка: назва поля не визначена.")
        return EDIT_DATA

    # Визначаємо тип поля для валідації
    field_type = determine_field_type(field_name)

    # Валідація введеного значення
    is_valid = True
    error_message = ""

    if field_type == 'date':
        is_valid, error_key = validate_date(new_value, field_name)
        if error_key and error_key in ui_text:
            error_message = ui_text[error_key]
        elif error_key:
            error_message = f"Помилка валідації дати: {error_key}"
    elif field_type == 'subject':
        is_valid, error_key = validate_subject(new_value)
        if error_key and error_key in ui_text:
            error_message = ui_text[error_key]
        elif error_key:
            error_message = f"Помилка валідації предмету: {error_key}"
    elif field_type == 'number':
        if not new_value.isdigit() or int(new_value) <= 0:
            is_valid = False
            error_message = ui_text.get('invalid_number', "Будь ласка, введіть коректне число.")
    elif field_type == 'phone':
        if not new_value.startswith('+') or not new_value[1:].isdigit() or len(new_value) < 10:
            is_valid = False
            error_message = ui_text.get('invalid_phone_format', "Будь ласка, введіть номер телефону у форматі +XXXXXXXXXXXX...")
    else: # Default to text validation
        min_length = 5 # Можна зробити параметр конфігурації або отримувати з метаданих поля
        is_valid, error_key = validate_text(new_value, min_length=min_length)
        if error_key and error_key in ui_text:
            error_message = ui_text[error_key].format(min_length=min_length)
        elif error_key:
            error_message = f"Помилка валідації тексту: {error_key}"

    if not is_valid:
        await update.message.reply_text(error_message)
        return EDIT_DATA

    user_data = user_data_store.get_user_data(user_id)
    if field_name in user_data.get('additional_data', {}):
        user_data['additional_data'][field_name] = new_value
    else:
        user_data[field_name] = new_value

    # Очищаємо дані від None та об’єктів, які можуть викликати цикли
    cleaned_data = {}
    for k, v in user_data.items():
        if k is None or v is None:
            continue
        if isinstance(v, (Update, CallbackContext)):
            continue
        cleaned_data[k] = v
    # Очищаємо additional_data
    cleaned_additional = {k: v for k, v in cleaned_data.get('additional_data', {}).items() if k is not None and v is not None}
    cleaned_data['additional_data'] = cleaned_additional

    user_data_store.set_user_data(user_id, None, cleaned_data)

    await update.message.reply_text(f"Значення для '{field_name}' оновлено на '{new_value}'.")
    return await display_confirmation(update, context, ui_builder, user_data_store)

async def cancel(update: Update, context: CallbackContext, data_loader, user_data_store) -> int:
    user = update.effective_user
    user_data_store.clear_user_data(user.id)
    await update.message.reply_text(data_loader.get_ui_text().get('cancel_message').format(first_name=user.first_name))
    return ConversationHandler.END
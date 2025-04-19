from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import os
from config import DOCUMENT, FULL_NAME, ADDITIONAL_DATA, CONFIRMATION, PHONE_NUMBER, REPEAT

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
            await context.bot.send_document(  # Використовуємо context.bot.send_document
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
        # Зберігаємо роль, факультет і кафедру, очищаємо інші дані
        user_data = user_data_store.get_user_data(user_id)
        role = user_data.get('role')
        faculty = user_data.get('faculty')
        department = user_data.get('department')
        user_data_store.clear_user_data(user_id)
        user_data_store.set_user_data(user_id, 'role', role)
        user_data_store.set_user_data(user_id, 'faculty', faculty)
        if department:
            user_data_store.set_user_data(user_id, 'department', department)


        # Повертаємося до вибору документів
        popular_docs = data_loader.get_popular_documents(role)
        all_docs = data_loader.get_documents(role)
        keyboard = [[InlineKeyboardButton(doc, callback_data=f'document_{doc}')] for doc in popular_docs]
        if all_docs and popular_docs != all_docs:
            keyboard.append([InlineKeyboardButton(data_loader.get_ui_text().get('all_documents_button'), callback_data='show_all_documents')])
        reply_markup = InlineKeyboardMarkup(keyboard)
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
    user_data_store.clear_user_data(user_id)
    await query.edit_message_text(data_loader.get_ui_text().get('data_change_prompt'))
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext, data_loader, user_data_store) -> int:
    user = update.effective_user
    user_data_store.clear_user_data(user.id)
    await update.message.reply_text(data_loader.get_ui_text().get('cancel_message').format(first_name=user.first_name))
    return ConversationHandler.END
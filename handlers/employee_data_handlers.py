from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from config import DOCUMENT, POSITION, EMP_ROLE, DEPARTMENT

async def department_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    department = query.data.split('_')[1]
    role = user_data_store[user_id].get('role')

    user_data_store[user_id]['department'] = department  # Зберігаємо кафедру безпосередньо

    if role == EMP_ROLE:
        positions = data_loader.get_positions()  # Отримайте список посад
        reply_markup = ui_builder.build_keyboard(positions, 'position_') # Зверніть увагу на зміну префікса
        current_selection = ui_builder.build_selection_text(user_data_store[user_id])
        message_text = f"{current_selection}\nБудь ласка, оберіть вашу посаду:"
        await query.edit_message_text(text=message_text, reply_markup=reply_markup)
        return POSITION
    return DEPARTMENT

async def position_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    position = query.data.split('_')[1]
    role = user_data_store[user_id].get('role')

    user_data_store[user_id]['position'] = position  # Зберігаємо посаду безпосередньо

    if role == EMP_ROLE:
        # Тепер можна переходити до вибору документа для працівника
        popular_docs = data_loader.get_popular_documents(role)
        all_docs = data_loader.get_documents(role)
        keyboard = [[InlineKeyboardButton(doc, callback_data=f'document_{doc}')] for doc in popular_docs]
        if all_docs and popular_docs != all_docs:
            keyboard.append([InlineKeyboardButton(data_loader.get_ui_text().get('all_documents_button'), callback_data='show_all_documents')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        current_selection = ui_builder.build_selection_text(user_data_store[user_id])
        message_text = f"{current_selection}\n{data_loader.get_ui_text().get('choose_document')}\n{data_loader.get_ui_text().get('popular_documents')}"
        await query.edit_message_text(text=message_text, reply_markup=reply_markup)
        return DOCUMENT
    return POSITION

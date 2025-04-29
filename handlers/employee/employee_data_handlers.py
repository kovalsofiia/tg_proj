# ADDED JSON SAVING easy alternative for saving data
from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from config import DOCUMENT, POSITION, EMP_ROLE, DEPARTMENT
from services.data_storage import DataStorage

async def department_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    department = query.data.split('_')[1]
    role = user_data_store.get_user_data(user_id).get('role')

    user_data_store.set_user_data(user_id, 'department', department)

    if role == EMP_ROLE:
        positions = data_loader.get_positions()
        reply_markup = ui_builder.build_keyboard(positions, 'position_')
        current_selection = ui_builder.build_selection_text(user_data_store.get_user_data(user_id))
        message_text = f"{current_selection}\nБудь ласка, оберіть вашу посаду:"
        await query.edit_message_text(text=message_text, reply_markup=reply_markup)
        return POSITION
    return DEPARTMENT

async def position_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    position = query.data.split('_')[1]
    role = user_data_store.get_user_data(user_id).get('role')

    user_data_store.set_user_data(user_id, 'position', position)

    if role == EMP_ROLE:
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
    return POSITION

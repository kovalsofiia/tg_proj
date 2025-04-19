# ADDED JSON SAVING easy alternative for saving data
from telegram.ext import CallbackContext
from telegram import Update
from config import ADDITIONAL_DATA, CONFIRMATION
from handlers.system.confirmation_handlers import display_confirmation
from utils.data_storage import DataStorage

async def show_all_documents(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> None:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    role = user_data_store.get_user_data(user_id).get('role')
    all_docs = data_loader.get_documents(role)
    reply_markup = ui_builder.build_all_documents_keyboard(all_docs)
    current_selection = ui_builder.build_selection_text(user_data_store.get_user_data(user_id))
    message_text = f"{current_selection}\n{data_loader.get_ui_text().get('choose_document')}"
    context.user_data['all_documents'] = {f'doc_id_{i}': doc for i, doc in enumerate(all_docs)}
    await query.edit_message_text(text=message_text, reply_markup=reply_markup)

async def document_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    chosen_document = query.data.split('_')[1]
    user_data_store.set_user_data(user_id, 'chosen_document', chosen_document)
    document_fields = data_loader.get_document_fields(chosen_document)
    if document_fields:
        first_field = document_fields[0]
        await query.edit_message_text(f"{ui_builder.build_selection_text(user_data_store.get_user_data(user_id))}\n{data_loader.get_ui_text().get('enter_your')} {first_field['label']}:")
        user_data_store.set_user_data(user_id, 'current_field', first_field['name'])
        return ADDITIONAL_DATA
    else:
        await display_confirmation(update, context, ui_builder, user_data_store)
        return CONFIRMATION
# from telegram.ext import CallbackContext
# from telegram import Update
# from config import ADDITIONAL_DATA,CONFIRMATION
# import re

# from handlers.system.confirmation_handlers import display_confirmation

# async def show_all_documents(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> None:
#     query = update.callback_query
#     await query.answer()
#     user_id = update.effective_user.id
#     role = user_data_store[user_id].get('role')
#     all_docs = data_loader.get_documents(role)
#     reply_markup = ui_builder.build_all_documents_keyboard(all_docs)
#     current_selection = ui_builder.build_selection_text(user_data_store[user_id])
#     message_text = f"{current_selection}\n{data_loader.get_ui_text().get('choose_document')}"
#     context.user_data['all_documents'] = {f'doc_id_{i}': doc for i, doc in enumerate(all_docs)}
#     await query.edit_message_text(text=message_text, reply_markup=reply_markup)

# async def document_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> int:
#     query = update.callback_query
#     await query.answer()
#     user_id = update.effective_user.id
#     chosen_document = query.data.split('_')[1]
#     user_data_store[user_id]['chosen_document'] = chosen_document
#     document_fields = data_loader.get_document_fields(chosen_document)
#     if document_fields:
#         first_field = document_fields[0]
#         await query.edit_message_text(f"{ui_builder.build_selection_text(user_data_store[user_id])}\n{data_loader.get_ui_text().get('enter_your')} {first_field['label']}:")
#         user_data_store[user_id]['current_field'] = first_field['name']  # Зберігаємо назву поля для введення
#         return ADDITIONAL_DATA
#     else:
#         await display_confirmation(update, context, ui_builder, user_data_store)
#         return CONFIRMATION
#     # query = update.callback_query
#     # await query.answer()
#     # user_id = update.effective_user.id
#     # callback_data = query.data
#     # if callback_data.startswith('doc_id_'):
#     #     document = context.user_data['all_documents'][callback_data]
#     # else:
#     #     document = callback_data.split('_')[1]
#     # user_data_store[user_id]['document'] = document

#     # # Отримуємо повний список полів для запитання при кожному виборі документа
#     # fields_to_ask = data_loader.get_document_fields(document)
#     # context.user_data['fields_to_ask'] = fields_to_ask[:] # Зберігаємо копію

#     # if fields_to_ask:
#     #     # Ініціалізуємо індекс поточного поля, яке запитуємо
#     #     context.user_data['current_field_index'] = 0
#     #     first_field = fields_to_ask[0]
#     #     await query.edit_message_text(f"{ui_builder.build_selection_text(user_data_store[user_id])}\n{data_loader.get_ui_text().get('enter_your')} {first_field['label']}:")
#     #     return ADDITIONAL_DATA
#     # else:
#     #     return await display_confirmation(update, context, ui_builder, user_data_store)
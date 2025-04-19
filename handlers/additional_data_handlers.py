# ADDED JSON SAVING easy alternative for saving data
from telegram.ext import CallbackContext
from telegram import Update
from config import ADDITIONAL_DATA
from handlers.system.confirmation_handlers import display_confirmation
from utils.data_storage import DataStorage

async def additional_data_received(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    user_id = update.effective_user.id
    fields_to_ask = context.user_data.get('fields_to_ask')
    current_field_index = context.user_data.get('current_field_index', 0)

    if not fields_to_ask or current_field_index >= len(fields_to_ask):
        # У випадку помилки або якщо всі поля вже опрацьовано
        return await display_confirmation(update, context, ui_builder, user_data_store)

    current_field = fields_to_ask[current_field_index]
    field_name = current_field['name']
    field_value = update.message.text

    # Отримуємо дані користувача
    user_data = user_data_store.get_user_data(user_id)
    if 'additional_data' not in user_data:
        user_data_store.set_user_data(user_id, 'additional_data', {})
    # Оновлюємо additional_data
    user_data_store.set_user_data(user_id, 'additional_data', {
        **user_data_store.get_user_data(user_id).get('additional_data', {}),
        field_name: field_value
    })

    context.user_data['current_field_index'] += 1

    if context.user_data['current_field_index'] < len(fields_to_ask):
        next_field = fields_to_ask[context.user_data['current_field_index']]
        await update.message.reply_text(f"{ui_builder.build_selection_text(user_data_store.get_user_data(user_id))}\n{data_loader.get_ui_text().get('enter_your')} {next_field['label']}:")
        return ADDITIONAL_DATA
    else:
        return await display_confirmation(update, context, ui_builder, user_data_store)
# from telegram.ext import CallbackContext
# from telegram import Update
# from config import ADDITIONAL_DATA

# from handlers.system.confirmation_handlers import display_confirmation

# async def additional_data_received(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> int:
#     user_id = update.effective_user.id
#     fields_to_ask = context.user_data.get('fields_to_ask')
#     current_field_index = context.user_data.get('current_field_index', 0)

#     if not fields_to_ask or current_field_index >= len(fields_to_ask):
#         # У випадку помилки або якщо всі поля вже опрацьовано
#         return await display_confirmation(update, context, ui_builder, user_data_store)

#     current_field = fields_to_ask[current_field_index]
#     field_name = current_field['name']
#     field_value = update.message.text

#     if 'additional_data' not in user_data_store[user_id]:
#         user_data_store[user_id]['additional_data'] = {}
#     user_data_store[user_id]['additional_data'][field_name] = field_value

#     context.user_data['current_field_index'] += 1

#     if context.user_data['current_field_index'] < len(fields_to_ask):
#         next_field = fields_to_ask[context.user_data['current_field_index']]
#         await update.message.reply_text(f"{ui_builder.build_selection_text(user_data_store[user_id])}\n{data_loader.get_ui_text().get('enter_your')} {next_field['label']}:")
#         return ADDITIONAL_DATA
#     else:
#         return await display_confirmation(update, context, ui_builder, user_data_store)
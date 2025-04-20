from telegram.ext import CallbackContext
from telegram import Update
from config import ADDITIONAL_DATA, CONFIRMATION
from handlers.system.confirmation_handlers import display_confirmation
from utils.data_storage import DataStorage

async def additional_data_received(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    user_id = update.effective_user.id
    field = context.user_data['fields_to_ask'][0]
    field_name = field['name']
    field_value = update.message.text
    user_data = user_data_store.get_user_data(user_id)
    if 'additional_data' not in user_data:
        user_data_store.set_user_data(user_id, 'additional_data', {})
    additional_data = user_data_store.get_user_data(user_id).get('additional_data', {})
    additional_data[field_name] = field_value
    user_data_store.set_user_data(user_id, 'additional_data', additional_data)
    context.user_data['fields_to_ask'].pop(0)
    if context.user_data['fields_to_ask']:
        next_field = context.user_data['fields_to_ask'][0]
        await update.message.reply_text(
            f"{ui_builder.build_selection_text(user_data_store.get_user_data(user_id))}\n{data_loader.get_ui_text().get('enter_your')} {next_field['label']}:"
        )
        return ADDITIONAL_DATA
    else:
        await display_confirmation(update, context, ui_builder, user_data_store)
        return CONFIRMATION

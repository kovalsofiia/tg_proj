from telegram.ext import CallbackContext
from telegram import Update
from config import ADDITIONAL_DATA, CONFIRMATION
from handlers.system.confirmation_handlers import display_confirmation
from handlers.additional_data_handlers import prepare_additional_fields
from utils.data_storage import DataStorage

async def prompt_for_field(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage, user_id: int, field: dict) -> None:
    """Prompt user for a specific field."""
    await update.callback_query.edit_message_text(
        f"{ui_builder.build_selection_text(user_data_store.get_user_data(user_id))}\n{data_loader.get_ui_text().get('enter_your')} {field['label']}:"
    )

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
    callback_data = query.data
    if callback_data.startswith('doc_id_'):
        document = context.user_data['all_documents'][callback_data]
    else:
        document = callback_data.split('_')[1]
    user_data_store.set_user_data(user_id, 'document', document)

    # Prepare fields to ask, excluding those already in user_data
    context.user_data['fields_to_ask'] = await prepare_additional_fields(context, document, data_loader, user_data_store, user_id)

    if context.user_data['fields_to_ask']:
        first_field = context.user_data['fields_to_ask'][0]  # Don't pop, just access the first field
        await prompt_for_field(update, context, data_loader, ui_builder, user_data_store, user_id, first_field)
        return ADDITIONAL_DATA
    else:
        await display_confirmation(update, context, ui_builder, user_data_store)
        return CONFIRMATION
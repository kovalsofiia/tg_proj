from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardMarkup
from utils.data_storage import DataStorage

async def save_and_proceed(
    update: Update,
    context: CallbackContext,
    user_data_store: DataStorage,
    user_id: int,
    key: str,
    value: str,
    next_state: int,
    message_text: str,
    reply_markup: Optional[InlineKeyboardMarkup] = None
) -> int:
    """Save user data and proceed to the next step.
    
    Args:
        update: Telegram update object.
        context: Telegram callback context.
        user_data_store: Data storage instance.
        user_id: User ID.
        key: Key to store in user data.
        value: Value to store.
        next_state: Next state to transition to.
        message_text: Message to send to the user.
        reply_markup: Optional keyboard markup.
    
    Returns:
        int: Next state.
    """
    user_data_store.set_user_data(user_id, key, value)
    if update.callback_query:
        await update.callback_query.edit_message_text(text=message_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=message_text, reply_markup=reply_markup)
    return next_state
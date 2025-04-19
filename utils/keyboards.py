from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

def get_phone_keyboard():
    keyboard = [[KeyboardButton("Поділитися номером телефону", request_contact=True)]]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

def build_inline_keyboard(items: list, prefix: str) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(item, callback_data=f'{prefix}{item}')] for item in items]
    return InlineKeyboardMarkup(keyboard)

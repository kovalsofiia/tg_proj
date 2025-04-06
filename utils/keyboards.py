from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
# Допоміжна функція для створення клавіатури телефону (можливо, її варто винести в окремий utils)
def get_phone_keyboard():
    keyboard = [[KeyboardButton("Поділитися номером телефону", request_contact=True)]]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from typing import List, Optional

def build_paginated_keyboard(
    items: List[str],
    prefix: str,
    items_per_row: int = 2,
    page: int = 1,
    items_per_page: int = 10
) -> InlineKeyboardMarkup:
    """Build a paginated keyboard for Telegram inline buttons.
    
    Args:
        items: List of items to display as buttons.
        prefix: Prefix for callback_data.
        items_per_row: Number of buttons per row.
        page: Current page number.
        items_per_page: Number of items per page.
    
    Returns:
        InlineKeyboardMarkup: Paginated keyboard.
    """
    start = (page - 1) * items_per_page
    end = start + items_per_page
    keyboard = [
        [InlineKeyboardButton(item, callback_data=f"{prefix}{item}") for item in items[i:i + items_per_row]]
        for i in range(start, min(end, len(items)), items_per_row)
    ]
    
    if len(items) > items_per_page:
        nav_buttons = []
        if page > 1:
            nav_buttons.append(InlineKeyboardButton("⬅️", callback_data=f"page_{page-1}_{prefix}"))
        if end < len(items):
            nav_buttons.append(InlineKeyboardButton("➡️", callback_data=f"page_{page+1}_{prefix}"))
        if nav_buttons:
            keyboard.append(nav_buttons)
    
    return InlineKeyboardMarkup(keyboard)

def get_phone_keyboard() -> InlineKeyboardMarkup:
    """Build a keyboard for requesting a phone number."""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Поділитися номером телефону", request_contact=True)]
    ])


# from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
# # Допоміжна функція для створення клавіатури телефону (можливо, її варто винести в окремий utils)
# def get_phone_keyboard():
#     keyboard = [[KeyboardButton("Поділитися номером телефону", request_contact=True)]]
#     return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

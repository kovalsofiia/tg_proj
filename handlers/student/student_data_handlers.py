from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from config import COURSE, SPECIALITY, EDUCATION_DEGREE, DOCUMENT, ST_ROLE
from services.data_storage import DataStorage

async def education_degree_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    degree = query.data.split('_')[1]
    role = user_data_store.get_user_data(user_id).get('role')

    user_data_store.set_user_data(user_id, 'education_degree', degree)

    if role == ST_ROLE:
        faculty = user_data_store.get_user_data(user_id).get('faculty')
        specialities = data_loader.get_departments(faculty, role=ST_ROLE)
        reply_markup = ui_builder.build_keyboard(specialities, 'speciality_')
        current_selection = ui_builder.build_selection_text(user_data_store.get_user_data(user_id))
        message_text = f"{current_selection}\nБудь ласка, оберіть вашу спеціальність:"
        await query.edit_message_text(text=message_text, reply_markup=reply_markup)
        return SPECIALITY
    return EDUCATION_DEGREE

import re

async def speciality_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    speciality_key = query.data.replace('speciality_', '')
    role = user_data_store.get_user_data(user_id).get('role')

    if role == ST_ROLE:
        # Знайдемо повну назву спеціальності за ключем
        faculty = user_data_store.get_user_data(user_id).get('faculty')
        specialities = data_loader.get_departments(faculty, role=ST_ROLE)
        speciality_name = next((name for key, name in specialities if key == speciality_key), speciality_key)
        
        # Розбиваємо спеціальність
        def split_speciality(speciality):
            pattern = r'^(\d+\.?\d*\.?\d*)\s*(.*)$'
            match = re.match(pattern, speciality)
            if match:
                code, name = match.groups()
                return code.strip(), name.strip()
            return '', speciality.strip()
        
        speciality_code, speciality_name_only = split_speciality(speciality_name)
        
        # Зберігаємо дані
        user_data_store.set_user_data(user_id, 'speciality', speciality_name)
        user_data_store.set_user_data(user_id, 'speciality_code', speciality_code)
        user_data_store.set_user_data(user_id, 'speciality_name', speciality_name_only)

        courses = ["1", "2", "3", "4", "5", "6"]
        reply_markup = ui_builder.build_keyboard(courses, 'course_')
        current_selection = ui_builder.build_selection_text(user_data_store.get_user_data(user_id))
        message_text = f"{current_selection}\nБудь ласка, оберіть ваш курс:"
        await query.edit_message_text(text=message_text, reply_markup=reply_markup)
        return COURSE
    return SPECIALITY

async def course_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    course = query.data.split('_')[1]
    role = user_data_store.get_user_data(user_id).get('role')

    user_data_store.set_user_data(user_id, 'course', course)

    if role == ST_ROLE:
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
    return COURSE
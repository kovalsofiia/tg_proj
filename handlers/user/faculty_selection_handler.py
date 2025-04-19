# ADDED JSON SAVING easy alternative for saving data
from telegram.ext import CallbackContext
from telegram import Update
from config import EDUCATION_DEGREE, DEPARTMENT, EMP_ROLE, ST_ROLE
from utils.data_storage import DataStorage

async def faculty_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store: DataStorage) -> int:
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    faculty = query.data.split('_')[1]
    role = user_data_store.get_user_data(user_id).get('role')

    user_data_store.set_user_data(user_id, 'faculty', faculty)

    if role == ST_ROLE:
        degrees = data_loader.get_education_degrees()
        reply_markup = ui_builder.build_keyboard(degrees, 'degree_')
        current_selection = ui_builder.build_selection_text(user_data_store.get_user_data(user_id))
        message_text = f"{current_selection}\nБудь ласка, оберіть ваш освітній ступінь:"
        await query.edit_message_text(text=message_text, reply_markup=reply_markup)
        return EDUCATION_DEGREE
    elif role == EMP_ROLE:
        departments = data_loader.get_departments(faculty)
        reply_markup = ui_builder.build_keyboard(departments, 'department_')
        current_selection = ui_builder.build_selection_text(user_data_store.get_user_data(user_id))
        message_text = f"{current_selection}\nБудь ласка, оберіть вашу кафедру:"
        await query.edit_message_text(text=message_text, reply_markup=reply_markup)
        return DEPARTMENT
    
# from telegram.ext import CallbackContext
# from telegram import Update
# from config import EDUCATION_DEGREE, DEPARTMENT, EMP_ROLE, ST_ROLE

# async def faculty_chosen(update: Update, context: CallbackContext, data_loader, ui_builder, user_data_store) -> int:
#     query = update.callback_query
#     await query.answer()
#     user_id = update.effective_user.id
#     faculty = query.data.split('_')[1]
#     role = user_data_store[user_id].get('role')

#     user_data_store[user_id]['faculty'] = faculty  # Зберігаємо факультет безпосередньо

#     if role == ST_ROLE:
#         degrees = data_loader.get_education_degrees()  # Припускаємо, що є така функція
#         reply_markup = ui_builder.build_keyboard(degrees, 'degree_')
#         current_selection = ui_builder.build_selection_text(user_data_store[user_id])
#         message_text = f"{current_selection}\nБудь ласка, оберіть ваш освітній ступінь:"
#         await query.edit_message_text(text=message_text, reply_markup=reply_markup)
#         return EDUCATION_DEGREE
#     elif role == EMP_ROLE:
#         departments = data_loader.get_departments(faculty)
#         reply_markup = ui_builder.build_keyboard(departments, 'department_')
#         current_selection = ui_builder.build_selection_text(user_data_store[user_id])
#         message_text = f"{current_selection}\nБудь ласка, оберіть вашу кафедру:"
#         await query.edit_message_text(text=message_text, reply_markup=reply_markup)
#         return DEPARTMENT
from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import ROLE, FACULTY, DEPARTMENT, DOCUMENT, FULL_NAME, PHONE_NUMBER, EDUCATION_DEGREE, COURSE, SPECIALITY, ADDITIONAL_DATA, CONFIRMATION, REPEAT, POSITION

class ConversationManager:
    def __init__(self, application, data_loader, ui_builder, doc_generator, user_data_store):
        self.application = application
        self.data_loader = data_loader
        self.ui_builder = ui_builder
        self.doc_generator = doc_generator
        self.user_data_store = user_data_store

    def setup_handlers(self):
        from handlers.system.start_handler import start
        from handlers.user.role_selection_handler import role_chosen
        from handlers.user.phone_number_handler import get_phone_number
        from handlers.user.full_name_handler import get_full_name
        from handlers.user.faculty_selection_handler import faculty_chosen
        from handlers.student_data_handlers import education_degree_chosen, speciality_chosen, course_chosen
        from handlers.employee_data_handlers import position_chosen, department_chosen
        from handlers.document_selection_handler import show_all_documents, document_chosen
        from handlers.additional_data_handlers import additional_data_received
        from handlers.system.confirmation_handlers import display_confirmation, format_chosen, confirm_data, change_data, cancel, repeat_choice

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", lambda u, c: start(u, c, self.data_loader, self.ui_builder, self.user_data_store))],
            states={
                ROLE: [CallbackQueryHandler(lambda u, c: role_chosen(u, c, self.data_loader, self.ui_builder, self.user_data_store), pattern='^role_')],
                FULL_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: get_full_name(u, c, self.data_loader, self.ui_builder, self.user_data_store))],
                PHONE_NUMBER: [
                    MessageHandler(filters.CONTACT | (filters.TEXT & ~filters.COMMAND), 
                                 lambda u, c: get_phone_number(u, c, self.data_loader, self.ui_builder, self.user_data_store))
                ],
                FACULTY: [CallbackQueryHandler(lambda u, c: faculty_chosen(u, c, self.data_loader, self.ui_builder, self.user_data_store), pattern='^faculty_')],
                EDUCATION_DEGREE: [CallbackQueryHandler(lambda u, c: education_degree_chosen(u, c, self.data_loader, self.ui_builder, self.user_data_store), pattern='^degree_')],
                SPECIALITY: [CallbackQueryHandler(lambda u, c: speciality_chosen(u, c, self.data_loader, self.ui_builder, self.user_data_store), pattern='^speciality_')],
                COURSE: [CallbackQueryHandler(lambda u, c: course_chosen(u, c, self.data_loader, self.ui_builder, self.user_data_store), pattern='^course_')],
                DEPARTMENT: [CallbackQueryHandler(lambda u, c: department_chosen(u, c, self.data_loader, self.ui_builder, self.user_data_store), pattern='^department_')],
                POSITION: [CallbackQueryHandler(lambda u, c: position_chosen(u, c, self.data_loader, self.ui_builder, self.user_data_store), pattern='^position_')],
                DOCUMENT: [
                    CallbackQueryHandler(lambda u, c: document_chosen(u, c, self.data_loader, self.ui_builder, self.user_data_store), 
                                      pattern=lambda data: data.startswith('document_') or data.startswith('doc_id_')),
                    CallbackQueryHandler(lambda u, c: show_all_documents(u, c, self.data_loader, self.ui_builder, self.user_data_store), 
                                      pattern='^show_all_documents$')
                ],
                ADDITIONAL_DATA: [MessageHandler(filters.TEXT & ~filters.COMMAND, 
                                               lambda u, c: additional_data_received(u, c, self.data_loader, self.ui_builder, self.user_data_store))],
                CONFIRMATION: [
                    CallbackQueryHandler(lambda u, c: confirm_data(u, c, self.doc_generator, self.user_data_store), pattern='^confirm$'),
                    CallbackQueryHandler(lambda u, c: change_data(u, c, self.data_loader), pattern='^change$'),
                    CallbackQueryHandler(lambda u, c: format_chosen(u, c, self.ui_builder, self.user_data_store), pattern='^format_'),
                    CallbackQueryHandler(lambda u, c: display_confirmation(u, c, self.ui_builder, self.user_data_store), pattern='^display$'),
                ],
                REPEAT: [CallbackQueryHandler(lambda u, c: repeat_choice(u, c, self.data_loader, self.ui_builder, self.user_data_store), pattern='^repeat_')],
            },
            fallbacks=[CommandHandler("cancel", lambda u, c: cancel(u, c, self.data_loader, self.user_data_store))],
        )
        self.application.add_handler(conv_handler)
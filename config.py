import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PHONE_NUMBER_REGEX = r'^(\+380|\b380|\b0)[0-9]{2}[\s-]?[0-9]{3}[\s-]?[0-9]{2}[\s-]?[0-9]{2}$'
DOCUMENT = 'document'
SPECIALITY = 'speciality'
COURSE = 'course'
SCIENTIFIC_DEGREE = 'scientific_degree'
POSITION = 'position'
ADDITIONAL_DATA = 'additional_data'
CONFIRMATION = 'confirmation'
REPEAT = 'repeat'

# Стани розмови
ROLE = 'ROLE'
FULL_NAME = 'FULL_NAME'
PHONE_NUMBER = 'PHONE_NUMBER'
FACULTY = 'FACULTY'
EDUCATION_DEGREE = 'EDUCATION_DEGREE'
DEPARTMENT = 'DEPARTMENT'

# Ролі
ST_ROLE = 'Студент'
EMP_ROLE = 'Працівник університету'

# Регулярний вираз для ПІБ
FULL_NAME_REGEX = r'^[А-ЯЇЄІҐ][а-яїєіґ]{2,} [А-ЯЇЄІҐ][а-яїєіґ]{2,} [А-ЯЇЄІҐ][а-яїєіґ]{2,}$'
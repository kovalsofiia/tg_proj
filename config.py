import os
from dotenv import load_dotenv

load_dotenv()

EMP_ROLE = 'Працівник університету'
ST_ROLE = 'Студент'
BOT_TOKEN = os.getenv("BOT_TOKEN")
FULL_NAME_REGEX = r'^[А-ЯЇЄІҐ][а-яїєіґ]{2,} [А-ЯЇЄІҐ][а-яїєіґ]{2,} [А-ЯЇЄІҐ][а-яїєіґ]{2,}$'
PHONE_NUMBER_REGEX = r'^(\+380|\b380|\b0)[0-9]{2}[\s-]?[0-9]{3}[\s-]?[0-9]{2}[\s-]?[0-9]{2}$'
# Стани розмови
ROLE = 'role'
FULL_NAME = 'full_name'
PHONE_NUMBER = 'phone_number'
FACULTY = 'faculty'
DEPARTMENT = 'department'
DOCUMENT = 'document'
EDUCATION_DEGREE = 'education_degree'
SPECIALITY = 'speciality'
COURSE = 'course'
SCIENTIFIC_DEGREE = 'scientific_degree'
POSITION = 'position'
ADDITIONAL_DATA = 'additional_data'
CONFIRMATION = 'confirmation'
REPEAT = 'repeat'
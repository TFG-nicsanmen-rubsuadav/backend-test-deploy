from datetime import datetime
import re

# local imports
from .constants import (
    EMAIL_ALREADY_IN_USE,
    PASSWORD_SPECIAL_CHAR,
    PHONE_ALREADY_IN_USE,
    WRONG_EMAIL, NAME_LENGTH,
    LAST_NAME_LENGTH, PHONE_MALFORMED,
    BIRTH_DATE_FORMAT, PASSWORD_LENGTH,
    PASSWORD_LOWERCASE,
    PASSWORD_UPPERCASE,
    PASSWORD_DIGIT,
    ROLE_LENGTH,
    ROLES, ROLE_NOT_ALLOWED
)

from conf.firebase import firestore


def validate_unique_email(email):
    emails = firestore.collection("users").stream()
    for e in emails:
        if e.to_dict()["email"] == email:
            raise ValueError(EMAIL_ALREADY_IN_USE)


def validate_unique_phone(phone):
    phones = firestore.collection("users").stream()
    for p in phones:
        if p.to_dict()["phone"] == phone:
            raise ValueError(PHONE_ALREADY_IN_USE)


def validate_user_creation(user):
    validate_unique_email(user["email"])
    validate_unique_phone(user["phone"])
    email_regex = r'^\w+([.-]?\w+)*@(gmail|hotmail|outlook)\.com$'
    phone_regex = r'^(\\+34|0034|34)?[ -]*(6|7)[ -]*([0-9][ -]*){8}$'
    if not re.match(email_regex, user["email"]):
        raise ValueError(WRONG_EMAIL)

    if len(user["name"]) < 3:
        raise ValueError(NAME_LENGTH)

    if len(user['last_name']) < 3:
        raise ValueError(LAST_NAME_LENGTH)

    if not re.match(phone_regex, user['phone']):
        raise ValueError(PHONE_MALFORMED)

    try:
        datetime.strptime(user['birth_date'], '%d/%m/%Y')
    except ValueError:
        raise ValueError(BIRTH_DATE_FORMAT)

    password = user['password']
    if len(password) < 8:
        raise ValueError(PASSWORD_LENGTH)
    if not re.search('[a-z]', password):
        raise ValueError(PASSWORD_LOWERCASE)
    if not re.search('[A-Z]', password):
        raise ValueError(PASSWORD_UPPERCASE)
    if not re.search('[0-9]', password):
        raise ValueError(PASSWORD_DIGIT)
    if not re.search('[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError(PASSWORD_SPECIAL_CHAR)


def get_allowed_roles(role: str):
    if role not in ROLES:
        raise ValueError(ROLE_NOT_ALLOWED)


def validate_role_creation(rol: str):
    if len(rol) < 3:
        raise ValueError(ROLE_LENGTH)


def check_roles(rol: str) -> str | bool:
    roles = firestore.collection("roles").stream()
    for r in roles:
        if r.to_dict()["name"] == rol:
            return r.id
    return False

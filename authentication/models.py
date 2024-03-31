# local imports
from .utils import validate_user_creation
from conf.firebase import firestore


def create_user(user):
    try:
        validate_user_creation(user)
        firestore.collection("users").add({
            "name": user["name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "phone": user["phone"],
            "birth_date": user["birth_date"],
            "password": user["password"]
        })
    except ValueError as e:
        raise e

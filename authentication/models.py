# local imports
from .utils import validate_user_creation, validate_role_creation, check_roles, get_allowed_roles
from conf.firebase import firestore


# Role model
def create_role(role: str):
    get_allowed_roles(role)
    role_id = check_roles(role)
    if role_id:
        return role_id
    else:
        try:
            validate_role_creation(role)
            _, role_ref = firestore.collection("roles").add({
                "name": role
            })
            return role_ref.id
        except ValueError as e:
            raise e


# User model
def create_user(user: dict, role_id: str | None = None):
    try:
        validate_user_creation(user)
        _, user_ref = firestore.collection("users").add({
            "name": user["name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "phone": user["phone"],
            "birth_date": user["birth_date"],
            "password": user["password"]
        })
        asociate_rol_with_user(user_ref.id, user["rol"], role_id)
    except ValueError as e:
        raise e


# Relationship between user and role
def asociate_rol_with_user(user_id: str, rol: str, role_id: str | None = None):
    firestore.document("users", user_id, "role", role_id).set({
        "name": rol
    })

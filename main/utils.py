def refactor_phone_number(phone_number: str):
    # Remove +34 from phone number if it exists
    if phone_number.startswith("+34"):
        phone_number = phone_number[3:]
    # Remove spaces from phone number
    phone_number = phone_number.replace(" ", "")
    # Remove - from phone number
    phone_number = phone_number.replace("-", "")

    return phone_number

def check_acces(user_role, is_active):
    access = "denied"
    if user_role == "admin" and is_active:
        access = "granted"
    return access
import bcrypt


def hash_password(
    password: str,
) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode("utf-8")


def validate_password(
    password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode(),
    )

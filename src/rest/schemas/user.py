import re

from pydantic import BaseModel, field_validator, ConfigDict


class RegistrationForm(BaseModel):
    username: str
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if len(v) < 5 or len(v) > 16:
            raise ValueError("Логин должен быть длиной между 5 и 16 символами.")
        if not re.match(r"^[a-zA-Z][a-zA-Z\d_]*$", v):
            raise ValueError("Разрешены только латиница, цифры и подчеркивания.")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Пароль должен содержать минимум 6 символов.")
        if not re.search(r"[a-z]", v):
            raise ValueError(
                "Пароль должен содержать хотя бы одну строчную латинскую букву."
            )
        if not re.search(r"\d", v):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")
        if not re.fullmatch(r"[A-Za-z0-9\W_]+", v):
            raise ValueError(
                "Пароль может содержать только латиницу, цифры и спецсимволы."
            )
        return v


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str

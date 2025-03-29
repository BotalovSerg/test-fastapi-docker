from pydantic import BaseModel


# Модель запроса для номера телефона
class PhoneRequest(BaseModel):
    phone: str
    api_id: str
    api_hash: str


# Модель запроса для ввода кода
class CodeRequest(BaseModel):
    phone: str
    code: str


# Модель запроса для облачного пароля (2FA)
class PasswordRequest(BaseModel):
    phone: str
    password: str

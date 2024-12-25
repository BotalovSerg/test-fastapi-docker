from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    telegram_id: int


class CVSchema(BaseModel):
    file_id: str

from odmantic import ObjectId
from pydantic import BaseModel, EmailStr, constr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)


class UserUpdate(BaseModel):
    name: str | None = None


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str


class UserPublic(BaseModel):
    id: ObjectId
    name: str
    email: str

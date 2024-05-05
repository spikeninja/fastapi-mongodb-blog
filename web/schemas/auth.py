from typing import Literal

from pydantic import BaseModel, EmailStr, constr

from schemas.user import UserPublic


class TwoFAResponse(BaseModel):
    user_id: str
    two_fa: bool


class SendCodeRequest(BaseModel):
    user_id: str
    send_method: Literal['email']


class CodeRequest(BaseModel):
    user_id: str
    code: str


class AuthResponse(BaseModel):
    access_token: str
    user: UserPublic


class LoginRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class ChangePassword(BaseModel):
    old_password: str
    new_password: str

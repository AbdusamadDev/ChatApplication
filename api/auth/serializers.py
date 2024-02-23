from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """Basic User authentication serializer"""

    username: str
    password: str


class UserRegistration(BaseModel):
    """Basic User registration serializer"""

    username: str
    email: EmailStr
    password: str


class TokenData(BaseModel):
    token: str
    token_type: str


class UserInfo(BaseModel):
    id: int
    username: str
    email: str


class MessageResponse(BaseModel):
    message: str

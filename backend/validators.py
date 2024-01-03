from pydantic import BaseModel, EmailStr


class MessagingBody(BaseModel):
    message: str
    chat_id: int

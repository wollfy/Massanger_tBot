from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class MessageCreate(BaseModel):
    sender_id: int  # Добавляем идентификатор отправителя
    receiver_id: int
    content: str
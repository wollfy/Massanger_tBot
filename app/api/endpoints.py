from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.models.message import Message
from app.schemas import UserCreate, UserOut, MessageCreate, UserLogin
from app.database import get_db

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code = status.HTTP_201_CREATED)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Проверка, что пользователь не существует
    result = await db.execute(select(User).filter(User.username == user.username))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Создание нового пользователя
    db_user = User(username=user.username)
    db_user.set_password(user.password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    # Выполнение запроса для поиска пользователя по имени
    result = await db.execute(select(User).filter(User.username == user.username))
    db_user = result.scalars().first()

    # Проверка существования пользователя и правильности пароля
    if db_user is None or not db_user.check_password(user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    return {"message": "Login successful"}


@router.post("/messages/send", status_code=status.HTTP_201_CREATED)
async def send_message(message: MessageCreate, db: AsyncSession = Depends(get_db)):
    # Проверка существования отправителя
    sender_result = await db.execute(select(User).filter(User.id == message.sender_id))
    sender = sender_result.scalars().first()

    if sender is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sender not found")

    # Проверка существования получателя
    receiver_result = await db.execute(select(User).filter(User.id == message.receiver_id))
    receiver = receiver_result.scalars().first()

    if receiver is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receiver not found")

    # Создание и сохранение сообщения
    db_message = Message(sender_id=message.sender_id, receiver_id=message.receiver_id, content=message.content)
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)

    return {"status": "Message sent", "message_id": db_message.id}
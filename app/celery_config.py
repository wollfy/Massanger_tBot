import os
from celery import Celery

# Получение настроек из переменных окружения
BROKER_URL = os.getenv("BROKER_URL", "redis://localhost:6379/0")
BACKEND_URL = os.getenv("BACKEND_URL", "redis://localhost:6379/0")

# Создание экземпляра Celery
celery = Celery('app', broker=BROKER_URL, backend=BACKEND_URL)

@celery.task
def send_telegram_notification(user_id, message):
    # Логика отправки уведомления через Telegram-бота
    print(f"Sending message to user {user_id}: {message}")

# Modern Messenger Platform

Современный мессенджер с расширенной функциональностью для эффективной коммуникации.

## 🚀 Особенности
- Микросервисная архитектура для обработки сообщений
- Система регистрации и авторизации пользователей
- Telegram-бот для уведомлений и отправки сообщений
- Асинхронная обработка задач с использованием Celery и Redis
- REST API на базе FastAPI

## 🛠️ Быстрый старт

### Требования
- Python 3.9+
- Redis Server
- Telegram API токен (для бота)

### Установка
1. Установите зависимости:
```bash
pip install -r requirements.txt

    Запустите Redis (в отдельном терминале):

bash
Copy

redis-server

    Запустите Celery worker (в отдельном терминале):

bash
Copy

celery -A tasks worker --loglevel=info

    Запустите Telegram-бота (в отдельном терминале):

bash
Copy

python app/bot.py

    Запустите основной сервер (в отдельном терминале):

bash
Copy

uvicorn app.main:app --reload

🐳 Docker-запуск
bash
Copy

docker-compose up --build

🔌 Портирование

    Основное приложение: http://localhost:8000

    Redis: 6379 (по умолчанию)

После запуска:
Приложение будет доступно по адресу: http://localhost:8000
Телеграм-бот начнет отвечать на сообщения при корректной настройке токена.

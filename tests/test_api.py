import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from app.main import app
from app.database import create_database, drop_database

@pytest.fixture(scope="module")
async def test_app():
    # Создание базы данных для тестов
    await create_database()  # Создайте базу данных
    yield app  # Возвращаем приложение для тестирования
    await drop_database()  # Удалите базу данных после тестов

@pytest.mark.asyncio
async def test_register(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        response = await client.post("/register", json={"username": "testuser", "password": "testpass"})
        assert response.status_code == 201
        assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_login(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        response = await client.post("/login", data={"username": "testuser", "password": "testpass"})
        assert response.status_code == 200
        assert response.json()["message"] == "Login successful"

@pytest.mark.asyncio
async def test_send_message(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        # Предположим, что у вас есть пользователь с id=1
        response = await client.post("/messages/send", data={"sender_id": 1, "receiver_id": 2, "content": "Hello!"})
        assert response.status_code == 201
        assert response.json()["status"] == "Message sent"
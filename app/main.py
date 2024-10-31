from fastapi import FastAPI
from app.database import engine, Base
from app.api.endpoints import router

app = FastAPI()

# Создание таблиц асинхронно
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(router, prefix="/api")

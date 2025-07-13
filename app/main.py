from fastapi import FastAPI
from .db import engine, Base
from sqlalchemy.exc import SQLAlchemyError
from . import models 
from .routers.hero import post_router, get_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except SQLAlchemyError as error:
        print("Ошибка при создании схемы БД:", error)
    yield
    await engine.dispose()

app = FastAPI(title="Heroes API", lifespan=lifespan)
app.include_router(post_router)
app.include_router(get_router)

@app.get("/")
async def root():
    return {"status": "running"}

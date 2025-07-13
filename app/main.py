from fastapi import FastAPI
from .db import engine, Base
from sqlalchemy.exc import SQLAlchemyError
from . import models 


app = FastAPI(title="Heroes API")

@app.get("/")
async def root():
    return {"status": "running"}

@app.on_event("startup")
async def on_startup():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except SQLAlchemyError as error:
        print("Ошибка при создании схемы БД:", error)

@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()

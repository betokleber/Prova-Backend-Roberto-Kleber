import os
from fastapi import FastAPI
from app.core.config import engine, Base
from app.routers import produtos

if os.getenv("ENV") != "testing":
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce API Modular - P2 Backend")

app.include_router(produtos.router)

from fastapi import FastAPI
from src.routes import users_router, rooms_router, auth_router

app = FastAPI()

app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(rooms_router, prefix="/api")


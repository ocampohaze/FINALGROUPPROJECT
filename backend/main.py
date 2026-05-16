from fastapi import FastAPI
from pydantic import BaseModel
from backend.auth import register_user, login_user
from backend.database import engine
from backend.database import Base

import backend.models


app = FastAPI()


# CREATE DATABASE TABLES
Base.metadata.create_all(bind=engine)


class User(BaseModel):
    username: str
    email: str = ""
    password: str


@app.get("/")
def home():
    return {"message": "API Working"}


@app.post("/register")
def register(user: User):

    return register_user(
        user.username,
        user.email,
        user.password
    )


@app.post("/login")
def login(user: User):

    return login_user(
        user.username,
        user.password
    )
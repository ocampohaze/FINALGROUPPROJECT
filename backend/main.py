from fastapi import FastAPI
from pydantic import BaseModel
from backend.auth import register_user, login_user

app = FastAPI()


class User(BaseModel):
    username: str
    email: str = ""
    password: str


@app.get("/")
def home():
    return {"message": "API Working"}


# REGISTER API
@app.post("/register")
def register(user: User):
    return register_user(user.username, user.email, user.password)


# LOGIN API
@app.post("/login")
def login(user: User):
    return login_user(user.username, user.password)

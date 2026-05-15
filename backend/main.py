from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()

# =========================
# FILE PATHS
# =========================

PRODUCTS_FILE = "products.csv"
USERS_FILE = "users.csv"

# =========================
# CREATE CSV FILES IF MISSING
# =========================

if not os.path.exists(PRODUCTS_FILE):
    products_df = pd.DataFrame(columns=[
        "id",
        "item_name",
        "category",
        "campus",
        "price",
        "seller"
    ])
    products_df.to_csv(PRODUCTS_FILE, index=False)

if not os.path.exists(USERS_FILE):
    users_df = pd.DataFrame(columns=[
        "id",
        "username",
        "password"
    ])
    users_df.to_csv(USERS_FILE, index=False)

# =========================
# PYDANTIC MODELS
# =========================

class Product(BaseModel):
    item_name: str
    category: str
    campus: str
    price: float
    seller: str

class User(BaseModel):
    username: str
    password: str

# =========================
# HOME ROUTE
# =========================

@app.get("/")
def home():
    return {"message": "RTU Marketplace Backend Running"}

# =========================
# REGISTER USER
# =========================

@app.post("/register")
def register(user: User):

    df = pd.read_csv(USERS_FILE)

    # CHECK IF USER EXISTS
    if user.username in df["username"].values:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_id = len(df) + 1

    new_user = {
        "id": new_id,
        "username": user.username,
        "password": user.password
    }

    df.loc[len(df)] = new_user

    df.to_csv(USERS_FILE, index=False)

    return {"message": "User registered successfully"}

# =========================
# LOGIN USER
# =========================

@app.post("/login")
def login(user: User):

    df = pd.read_csv(USERS_FILE)

    matched_user = df[
        (df["username"] == user.username) &
        (df["password"] == user.password)
    ]

    if matched_user.empty:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {"message": "Login successful"}

# =========================
# ADD PRODUCT
# =========================

@app.post("/add-product")
def add_product(product: Product):

    df = pd.read_csv(PRODUCTS_FILE)

    new_id = len(df) + 1

    new_product = {
        "id": new_id,
        "item_name": product.item_name,
        "category": product.category,
        "campus": product.campus,
        "price": product.price,
        "seller": product.seller
    }

    df.loc[len(df)] = new_product

    df.to_csv(PRODUCTS_FILE, index=False)

    return {"message": "Product added successfully"}

# =========================
# VIEW ALL PRODUCTS
# =========================

@app.get("/products")
def get_products():

    df = pd.read_csv(PRODUCTS_FILE)

    return df.to_dict(orient="records")

# =========================
# SEARCH PRODUCTS
# =========================

@app.get("/search")
def search_products(keyword: str):

    df = pd.read_csv(PRODUCTS_FILE)

    filtered = df[
        df["item_name"].str.contains(
            keyword,
            case=False,
            na=False
        )
    ]

    return filtered.to_dict(orient="records")

# =========================
# FILTER BY CAMPUS
# =========================

@app.get("/campus/{campus_name}")
def filter_campus(campus_name: str):

    df = pd.read_csv(PRODUCTS_FILE)

    filtered = df[
        df["campus"].str.lower() == campus_name.lower()
    ]

    return filtered.to_dict(orient="records")

# =========================
# DELETE PRODUCT
# =========================

@app.delete("/delete-product/{product_id}")
def delete_product(product_id: int):

    df = pd.read_csv(PRODUCTS_FILE)

    if product_id not in df["id"].values:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    df = df[df["id"] != product_id]

    df.to_csv(PRODUCTS_FILE, index=False)

    return {"message": "Product deleted successfully"}

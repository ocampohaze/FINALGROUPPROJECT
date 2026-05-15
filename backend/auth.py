import csv
import os

USER_FILE = "data/users_account.csv"


def init_file():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["user_id", "username", "email", "password"])


def register_user(username, email, password):
    init_file()

    with open(USER_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                return {"status": "error", "message": "Username already exists"}

    with open(USER_FILE, "r") as f:
        reader = list(csv.DictReader(f))
        user_id = str(len(reader) + 1)

    with open(USER_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user_id, username, email, password])

    return {"status": "success", "message": "Registered successfully"}


def login_user(username, password):
    init_file()

    with open(USER_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username and row["password"] == password:
                return {"status": "success", "user": row}

    return {"status": "error", "message": "Invalid login"}

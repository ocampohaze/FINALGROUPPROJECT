import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from backend.auth import register_user, login_user


st.title("Buy Sell Trade App")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])


# ---------------- REGISTER ----------------
if menu == "Register":
    st.subheader("Create Account")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        result = register_user(username, email, password)

        if result["status"] == "success":
            st.success(result["message"])
        else:
            st.error(result["message"])


# ---------------- LOGIN ----------------
if menu == "Login":
    st.subheader("Login Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        import requests
        result = requests.post("http://127.0.0.1:8000/login", json={
              "username": username,
              "password": password
              }).json()

        if result["status"] == "success":
            st.success("Login successful!")

            # store user session
            st.session_state["user"] = result["user"]

        else:
            st.error(result["message"])


# ---------------- DASHBOARD ----------------
if "user" in st.session_state:
    st.divider()
    st.subheader("Dashboard")

    user = st.session_state["user"]

    st.write("Welcome:", user["username"])
    st.write("Email:", user["email"])

    if st.button("Logout"):
        del st.session_state["user"]
        st.rerun()


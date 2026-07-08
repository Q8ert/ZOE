import streamlit as st
import json
import bcrypt
from pathlib import Path

USER_FILE = Path("users.json")

def load_user():
    if USER_FILE.exists():
        return json.loads(USER_FILE.read_text())
    return {}

def login(username, password):
    USER = load_user()
    if username not in USER:
        return False
    return bcrypt.checkpw(password.encode(), USER[username].encode())

def save_users(users):
    USER_FILE.write_text(json.dumps(users, indent=2))
 
 
def register(username, password):
    users = load_user()
    if username in users:
        return False
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[username] = hashed
    save_users(users)
    return True

def init_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
        
def login_page():
    st.title("User Page")
    
    login_tab, register_tab = st.tabs(["Log in", "Register"])
    
    with login_tab:
        username = st.text_input("Username", key="login_user", value="")
        password = st.text_input("Password", type="password", key="login_pass", value="")
        if st.button("Log in"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Wrong username or password")
                
    with register_tab:
        new_user = st.text_input("Choose a username", key="reg_user", placeholder="Username", value="")
        new_pass = st.text_input("Choose a password", type="password", key="reg_pass", placeholder="Password", value="")
        if st.button("Create account"):
            if not new_user or not new_pass:
                st.warning("Fill in both fields")
            elif register(new_user, new_pass):
                st.success("Account created. Switch to the Log in tab.")
            else:
                st.error("That username is already taken")
                
def home_page():
    st.title("My App")
    st.write(f"Welcome, **{st.session_state.username}**")
                
def main():
    init_state()
    if st.session_state.logged_in:
        home_page()
    else:
        login_page()
        
main()
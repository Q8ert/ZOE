import streamlit as st
import json
import bcrypt
from pathlib import Path

from symptoms import symptom_tracker
from reports import create_gp_report, create_in_the_moment_support

USER_FILE = Path("users.json")


def load_user():
    if USER_FILE.exists():
        return json.loads(USER_FILE.read_text())
    return {}


def login(username, password):
    users = load_user()
    if username not in users:
        return False
    return bcrypt.checkpw(password.encode(), users[username].encode())


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
    st.title("Seen Symptom Ally")

    login_tab, register_tab = st.tabs(["Log in", "Register"])

    with login_tab:
        username = st.text_input("Username", key="login_user", value="", placeholder="Username")
        password = st.text_input(
            "Password",
            type="password",
            key="login_pass",
            placeholder="Password",
            value="",
        )

        if st.button("Log in"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Wrong username or password")

    with register_tab:
        new_user = st.text_input(
            "Choose a username",
            key="reg_user",
            placeholder="Username",
            value="",
        )
        new_pass = st.text_input(
            "Choose a password",
            type="password",
            key="reg_pass",
            placeholder="Password",
            value="",
        )

        if st.button("Create account"):
            if not new_user or not new_pass:
                st.warning("Fill in both fields")
            elif register(new_user, new_pass):
                st.success("Account created. Switch to the Log in tab.")
            else:
                st.error("That username is already taken")


def home_page():
    st.title("Symptom Ally")
    st.write(f"Welcome, **{st.session_state.username}**")

    patient_context = symptom_tracker()

    if patient_context:
        st.divider()

        # Confirmation before generating support
        if st.button("Yes, this looks right — show me support"):
            if not st.session_state.logged_in:
                login_page()
            else:
                support = create_in_the_moment_support(patient_context)
                st.session_state["support"] = support

        # Button to create GP notes
        if st.button("Create my GP notes"):
            if not st.session_state.logged_in:
                login_page()
            else:
                gp_report = create_gp_report(patient_context)
                st.session_state["gp_report"] = gp_report

        # Show outputs in tabs to avoid long walls of text
        tabs = st.tabs(["Support", "GP notes"])

        with tabs[0]:
            if "support" in st.session_state:
                st.subheader("Support for right now")
                st.markdown(st.session_state["support"])
            else:
                st.info("Click 'Yes, this looks right — show me support' to get practical suggestions.")

        with tabs[1]:
            if "gp_report" in st.session_state:
                st.subheader("GP appointment notes")
                st.markdown(st.session_state["gp_report"])

                st.download_button(
                    "Download GP notes",
                    data=st.session_state["gp_report"],
                    file_name="gp_notes.md",
                    mime="text/markdown",
                )
            else:
                st.info("Click 'Create my GP notes' to generate concise notes you can bring to your appointment.")


def main():
    init_state()
    home_page()


main()
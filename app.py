from reports import create_gp_report, create_in_the_moment_support
import streamlit as st
import json
import bcrypt
from pathlib import Path

from symptoms import symptom_tracker
#from reports import create_gp_report, create_in_the_moment_support

USER_FILE = Path("users.json")


def load_user():
    if USER_FILE.exists():
        try:
            return json.loads(USER_FILE.read_text())
        except json.JSONDecodeError:
            return {}  # empty or corrupt file, treat as no users
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
    # UI state for auth landing
    if "show_login" not in st.session_state:
        st.session_state.show_login = False
    if "show_register" not in st.session_state:
        st.session_state.show_register = False


def login_page():
    st.title("Seen")

    st.write("Feel prepared. Feel heard.")

    st.write(
        "Seen helps you organise your symptoms, understand what matters most, "
        "and prepare for better conversations with your GP."
    )

    # helper callbacks
    def _show_login():
        st.session_state.show_login = True
        st.session_state.show_register = False

    def _show_register():
        st.session_state.show_register = True
        st.session_state.show_login = False

    def _back_to_landing():
        st.session_state.show_login = False
        st.session_state.show_register = False

    col1, col2 = st.columns(2)
    with col1:
        st.button("Log in", on_click=_show_login)
    with col2:
        st.button("Create account", on_click=_show_register)

    # Show the appropriate form when requested
    if st.session_state.show_login:
        st.markdown("---")
        st.subheader("Log in")

        username = st.text_input("Username", key="login_user", value="", placeholder="Username")
        password = st.text_input(
            "Password",
            type="password",
            key="login_pass",
            placeholder="Password",
            value="",
        )

        if st.button("Log in", key="do_login"):
            if login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Wrong username or password")

        if st.button("Back", key="back_from_login"):
            _back_to_landing()

    if st.session_state.show_register:
        st.markdown("---")
        st.subheader("Create account")

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

        if st.button("Create account", key="do_register"):
            if not new_user or not new_pass:
                st.warning("Fill in both fields")
            elif register(new_user, new_pass):
                st.success("Account created. You can now log in.")
                # After successful registration, show login form
                st.session_state.show_register = False
                st.session_state.show_login = True
            else:
                st.error("That username is already taken")

        if st.button("Back", key="back_from_register"):
            _back_to_landing()

def checkin_page():
    st.title("Seen Symptom Ally")
    st.write(f"Welcome, **{st.session_state.username}**")

    patient_context = symptom_tracker()


    if patient_context:
        st.divider()

        # Show the LLM confirmation summary
        if "confirmation_summary" in st.session_state:
            st.subheader("You've told us...")
            st.markdown(st.session_state["confirmation_summary"])

        # User confirms the summary before receiving support
        if st.button("Yes, this looks right — show me support"):

            with st.spinner("Creating personalised support..."):
                st.session_state["support"] = create_in_the_moment_support(
                    patient_context
                )

        # Show support once generated
        if "support" in st.session_state:
            st.divider()
            st.subheader("Support for right now")
        st.markdown(st.session_state["support"])

        # Only offer GP notes after support has been generated
        if st.button("Create my GP notes"):

            with st.spinner("Preparing your GP notes..."):
                st.session_state["gp_report"] = create_gp_report(
                    patient_context
                )

        # Show GP notes once generated
        if "gp_report" in st.session_state:
            st.divider()
            st.subheader("Your GP notes")
            st.markdown(st.session_state["gp_report"])

            st.download_button(
                "Download GP notes",
                data=st.session_state["gp_report"],
                file_name="gp_notes.md",
                mime="text/markdown",
            )


def main():
    init_state()

    if st.session_state.logged_in:
        checkin_page()
    else:
        login_page()

main()

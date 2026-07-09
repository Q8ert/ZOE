import streamlit as st
import json
import bcrypt
from pathlib import Path
import base64

from symptoms import symptom_tracker, save_user_progress, get_user_progress, PROGRESS_FILE
from reports import create_gp_report, create_in_the_moment_support
from blog import blog_page

USER_FILE = Path(__file__).resolve().parent / "users.json"
progress_file = Path("user_progress.json")
if not progress_file.exists():
    progress_file.write_text("{}")

def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    # 1) Background image
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{
            background: rgba(0, 0, 0, 0);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 2) Text and control colours.
    #    - Normal page text is dark (readable on the light background image).
    #    - Buttons and inputs get a solid surface with matching text colour,
    #      so nothing ends up dark-on-dark.
    st.markdown(
        """
        <style>
        /* Page text: dark, but ONLY the general content, not controls.
           We deliberately do NOT use a blanket "* { color: black }" rule,
           because that also blackened button labels and typed input text. */
        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] li,
        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stMarkdownContainer"] {
            color: #1a1a1a !important;
        }

        /* Buttons: white surface, dark label (label stays visible) */
        [data-testid="stButton"] button,
        [data-testid="stDownloadButton"] button,
        [data-testid="stFormSubmitButton"] button {
            background-color: #ffffff !important;
            border: 1px solid rgba(0,0,0,0.15) !important;
        }
        [data-testid="stButton"] button *,
        [data-testid="stDownloadButton"] button *,
        [data-testid="stFormSubmitButton"] button * {
            color: #1a1a1a !important;
        }
        [data-testid="stButton"] button:hover,
        [data-testid="stDownloadButton"] button:hover,
        [data-testid="stFormSubmitButton"] button:hover {
            background-color: #f2f2f2 !important;
        }

        /* Text inputs / text areas: white surface, dark typed text */
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
            background-color: #ffffff !important;
            color: #1a1a1a !important;
            -webkit-text-fill-color: #1a1a1a !important;
        }
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder {
            color: rgba(0,0,0,0.45) !important;
            -webkit-text-fill-color: rgba(0,0,0,0.45) !important;
        }

        /* Select / multiselect closed field: white surface, dark text */
        [data-baseweb="select"] > div {
            background-color: #ffffff !important;
        }
        [data-baseweb="select"] > div * {
            color: #1a1a1a !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

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


def ensure_progress_file():
    # Guarantee the progress file exists the moment the app starts, the same
    # way users.json exists. It starts as an empty object and gets filled in
    # as people save their check-ins.
    if not PROGRESS_FILE.exists():
        PROGRESS_FILE.write_text(json.dumps({}, indent=2))


def init_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None
    # show_auth decides whether we are on the home page (False) or the
    # login / create-account page (True). "Get started" flips it to True.
    if "show_auth" not in st.session_state:
        st.session_state.show_auth = False
    # view decides which logged-in screen shows: the check-in or the blog.
    if "view" not in st.session_state:
        st.session_state.view = "checkin"
    # UI state for the auth forms
    if "show_login" not in st.session_state:
        st.session_state.show_login = False
    if "show_register" not in st.session_state:
        st.session_state.show_register = False


def do_logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.show_auth = False      # back to the home page
    st.session_state.show_login = False
    st.session_state.show_register = False
    st.session_state.view = "checkin"       # reset the logged-in view
    for key in ("patient_context", "confirmation_summary", "support", "gp_report"):
        st.session_state.pop(key, None)
    st.rerun()


def home_page():
    # First screen everyone sees. No log in required to view it.

    # ---------- HERO ----------
    st.caption("A CALMER WAY THROUGH MENOPAUSE")
    st.title("You're not imagining it. You're not alone.")
    st.write(
        "Seen is a judgment-free space to track your symptoms, understand what's "
        "happening in your body, and talk to women who truly get it."
    )

    st.divider()

    # ---------- ABOUT (updated copy) ----------
    st.caption("ABOUT US")
    st.header("Built to help you feel seen, not dismissed")
    st.write(
        "Seen is a menopause support space built around one simple belief: your "
        "symptoms, questions, and lived experience deserve to be taken seriously. "
        "We help you log what is happening day by day, spot patterns over time, and "
        "turn those patterns into clearer support."
    )
    st.write(
        "Instead of generic advice, Seen connects you with Circles of people whose "
        "logged experiences overlap with yours. Peer tips are tagged by real "
        "outcomes, so you can learn what helped others, save useful questions, and "
        "walk into care conversations feeling more prepared."
    )
    a1, a2, a3 = st.columns(3)
    a1.info("Daily symptom logs")
    a2.info("Outcome-backed advice")
    a3.info("Matched Circles")

    st.divider()

    # ---------- MISSION ----------
    st.caption("OUR MISSION")
    st.subheader(
        "To make sure no woman goes through menopause feeling unseen, unheard, "
        "or alone."
    )
    pillars = [
        ("Track", "Log symptoms and gently spot the patterns behind them."),
        ("Understand", "Get trusted, personalised guidance for every stage."),
        ("Connect", "Join a warm community of women who just get it."),
    ]
    for col, (title, body) in zip(st.columns(3), pillars):
        with col:
            with st.container(border=True):
                st.markdown(f"### {title}")
                st.write(body)

    st.divider()

    # ---------- REVIEWS ----------
    st.caption("REVIEWS")
    st.header("What members are saying")
    reviews = [
        (
            "\u2b50\u2b50\u2b50\u2b50\u2b50",
            "I finally understood why I couldn't sleep. Seen gave me the language "
            "for what I was feeling, and that alone was a relief.",
            "Priya, 52",
        ),
        (
            "\u2b50\u2b50\u2b50\u2b50\u2b50",
            "The community is what keeps me coming back. No judgment, just women "
            "who genuinely get it.",
            "Marion, 49",
        ),
        (
            "\u2b50\u2b50\u2b50\u2b50",
            "My doctor appointments got so much easier once I had my symptom "
            "history tracked and ready to share.",
            "Dee, 55",
        ),
    ]
    for col, (stars, quote, who) in zip(st.columns(3), reviews):
        with col:
            with st.container(border=True):
                st.write(stars)
                st.write(f"\u201c{quote}\u201d")
                st.caption(who)

    st.divider()

    # ---------- CALL TO ACTION ----------
    st.caption("READY WHEN YOU ARE")
    st.header("Ready to feel seen?")
    st.write(
        "Join thousands of women navigating menopause with more clarity, and a "
        "lot more calm."
    )
    # Get started sends the user to the login / create-account screen.
    if st.button("Get started, it's free", key="cta_get_started", type="primary"):
        st.session_state.show_auth = True
        st.rerun()

    st.divider()
    st.caption("\u00a9 2026 Seen. All rights reserved.")


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
    # Sidebar navigation between the symptom check-in and the blog.
    st.sidebar.title("Seen")
    if st.sidebar.button("Symptom check-in", key="nav_checkin"):
        st.session_state.view = "checkin"
    if st.sidebar.button("BLOG", key="nav_blog"):
        st.session_state.view = "blog"
    if st.sidebar.button("Log out", key="logout_app"):
        do_logout()

    # Show the blog instead of the check-in when it is selected.
    if st.session_state.get("view") == "blog":
        blog_page()
        return

    st.title("Seen Symptom Ally")
    st.write(f"Welcome, **{st.session_state.username}**")

    username = st.session_state.get("username")

    # If this user already has saved answers in user_progress.json, load them
    # into the session the first time they land on this page. That makes
    # patient_context available straight away, so the two action buttons below
    # appear immediately, and any previously generated support / GP notes are
    # restored into the tabs.
    if username and "patient_context" not in st.session_state:
        saved = get_user_progress(username)
        if saved:
            st.session_state["patient_context"] = saved
            # Restore previously generated reports from disk, if present.
            if saved.get("support"):
                st.session_state["support"] = saved["support"]
            if saved.get("gp_report"):
                st.session_state["gp_report"] = saved["gp_report"]

    patient_context = symptom_tracker()

    # GUARANTEED SAVE: whenever there is check-in data and we know the user,
    # write it to the JSON file. checkin_page only runs when logged in, so the
    # username is always set here. patient_context can also carry the generated
    # support and GP notes (attached below), so those persist here as well.
    if patient_context and st.session_state.get("username"):
        save_user_progress(st.session_state["username"], patient_context)

    if patient_context:
        st.divider()

        # The report functions should only see the check-in data, not any
        # previously generated report text, so strip those keys before sending.
        context_for_model = {
            k: v for k, v in patient_context.items()
            if k not in ("support", "gp_report")
        }

        # One button each, no duplicates.
        if st.button("Yes, this looks right, show me support", key="gen_support"):
            with st.spinner("Creating personalised support..."):
                support = create_in_the_moment_support(context_for_model)
            st.session_state["support"] = support
            # SAVE the generated support into user_progress.json.
            patient_context["support"] = support
            if username:
                save_user_progress(username, patient_context)

        if st.button("Create my GP notes", key="gen_gp_report"):
            with st.spinner("Preparing your GP notes..."):
                gp_report = create_gp_report(context_for_model)
            st.session_state["gp_report"] = gp_report
            # SAVE the generated GP notes into user_progress.json.
            patient_context["gp_report"] = gp_report
            if username:
                save_user_progress(username, patient_context)

        tabs = st.tabs(["Support", "GP notes"])

        with tabs[0]:
            if "support" in st.session_state:
                st.subheader("Support for right now")
                st.markdown(st.session_state["support"])
            else:
                st.info("Click 'Yes, this looks right, show me support' to get practical suggestions.")

        with tabs[1]:
            if "gp_report" in st.session_state:
                st.subheader("GP appointment notes")
                st.markdown(st.session_state["gp_report"])
                st.download_button(
                    "Download GP notes",
                    data=st.session_state["gp_report"],
                    file_name="gp_notes.md",
                    mime="text/markdown",
                    key="download_gp",
                )
            else:
                st.info("Click 'Create my GP notes' once you're ready.")


def main():
    st.set_page_config(
        page_title="Seen",
        page_icon=str("icon.jpg"),
    )
    set_background("background.jpg")   # your image next to app.py
    init_state()
    ensure_progress_file()

    # Flow: home page  ->  (Get started)  ->  login  ->  report and profile.
    if st.session_state.logged_in:
        checkin_page()
    elif st.session_state.show_auth:
        login_page()
    else:
        home_page()


main()
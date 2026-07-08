import json
from pathlib import Path

import streamlit as st
from reports import create_confirmation_summary


PROGRESS_FILE = Path("user_progress.json")


# ----------------------------------------------------------------------
# Progress storage. One JSON file, keyed by username, so each logged-in
# person gets their own saved answers. The file is created on first save.
# Shape: { "luka": {patient_context...}, "someone": {patient_context...} }
# ----------------------------------------------------------------------
def load_all_progress():
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            return {}  # empty or corrupt file, treat as no saved progress
    return {}


def save_user_progress(username, patient_context):
    all_progress = load_all_progress()
    all_progress[username] = patient_context  # overwrite this user's entry
    PROGRESS_FILE.write_text(json.dumps(all_progress, indent=2))


def get_user_progress(username):
    return load_all_progress().get(username)


SYMPTOM_CATEGORIES = {
    "Sleep & energy": [
        "Sleep problems",
        "Fatigue",
        "Night sweats",
    ],
    "Mood & mind": [
        "Brain fog",
        "Memory problems",
        "Low mood",
        "Anxiety",
        "Irritability",
    ],
    "Periods & hormones": [
        "Irregular periods",
        "Heavy periods",
        "Hot flushes",
    ],
    "Body & physical symptoms": [
        "Joint pain",
        "Headaches",
        "Palpitations",
        "Digestive changes",
        "Weight changes",
        "Skin changes",
        "Hair changes",
    ],
    "Sexual & urinary health": [
        "Vaginal dryness",
        "Low libido",
        "Urinary symptoms",
    ],
}


DURATION_OPTIONS = [
    "Not selected",
    "Today",
    "A few days",
    "A few weeks",
    "A few months",
    "Longer than 6 months",
    "Not sure",
]


IMPACT_OPTIONS = [
    "Sleep",
    "Work or study",
    "Exercise or movement",
    "Mood",
    "Relationships",
    "Caring responsibilities",
    "Daily activities",
    "Confidence",
]


def symptom_tracker():
    st.header("Appointment preparation")

    st.write(
        "Start with the areas that feel relevant. "
        "You can add more detail only where you want to."
    )

    # Load previously saved answers for the logged-in user, if any exist.
    username = st.session_state.get("username")
    if username:
        saved = get_user_progress(username)
        if saved and st.button("Load my saved answers"):
            st.session_state["patient_context"] = saved
            st.success("Loaded your saved answers")

    with st.form("symptom_form"):
        st.subheader("1. Symptom areas")

        symptom_entries = []

        for category, symptoms in SYMPTOM_CATEGORIES.items():
            with st.expander(category):
                selected_symptoms = st.multiselect(
                    f"Which {category.lower()} symptoms are you experiencing?",
                    symptoms,
                    key=f"{category}_selected",
                )

                for symptom in selected_symptoms:
                    col1, col2 = st.columns(2)

                    with col1:
                        severity = st.slider(
                            f"{symptom} severity",
                            1,
                            5,
                            3,
                            key=f"{symptom}_severity",
                        )

                    with col2:
                        duration = st.selectbox(
                            f"{symptom} duration",
                            DURATION_OPTIONS,
                            key=f"{symptom}_duration",
                        )

                    symptom_entries.append(
                        {
                            "category": category,
                            "symptom": symptom,
                            "severity": severity,
                            "duration": duration,
                        }
                    )

        st.subheader("2. Impact")
        impact = st.multiselect(
            "How are these symptoms affecting your daily life?",
            IMPACT_OPTIONS,
        )

        st.subheader("3. Main concern")
        main_concern = st.text_area(
            "What are you most worried about?",
            placeholder="For example: I'm worried this isn't normal, or I'm struggling to cope at work.",
        )

        st.subheader("4. Appointment goal")
        appointment_goal = st.text_area(
            "What would you like to get out of today's appointment?",
            placeholder="For example: understand what's causing this, discuss options, get a referral, or rule something out.",
        )

        st.subheader("5. Anything else")
        additional_notes = st.text_area(
            "Anything else you'd like your GP to know?",
            placeholder="Patterns, triggers, what you've tried, or previous healthcare conversations.",
        )

        submitted = st.form_submit_button("Save check-in")

    if submitted:
        sorted_symptoms = sorted(
            symptom_entries,
            key=lambda item: item["severity"],
            reverse=True,
        )

        patient_context = {
            "symptoms": sorted_symptoms,
            "top_concerns": sorted_symptoms[:3],
            "impact": impact,
            "main_concern": main_concern,
            "appointment_goal": appointment_goal,
            "additional_notes": additional_notes,
        }

        st.session_state["patient_context"] = patient_context
        st.success("Check-in saved")

    patient_context = st.session_state.get("patient_context")

    if patient_context:
        # Generate or reuse an LLM confirmation summary
        if "confirmation_summary" not in st.session_state:
            try:
                summary = create_confirmation_summary(patient_context)
            except Exception:
                summary = "Sorry — we couldn't create a confirmation summary right now. Please check your entries."

            st.session_state["confirmation_summary"] = summary

        st.subheader("You've told us...")
        st.markdown(st.session_state["confirmation_summary"])

        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("Edit check-in"):
                # Allow user to edit their check-in: clear saved context and summary
                st.session_state.pop("patient_context", None)
                st.session_state.pop("confirmation_summary", None)
                st.experimental_rerun()

        with col2:
            st.caption("If this looks right, go to the main page and click 'Yes, this looks right — show me support'.")

        # Save this check-in to the logged-in user's account.
        st.divider()
        if username:
            if st.button("Save my progress to my account"):
                save_user_progress(username, patient_context)
                st.success("Progress saved to your account")
        else:
            st.info("Log in to save your progress to your account.")

    return patient_context
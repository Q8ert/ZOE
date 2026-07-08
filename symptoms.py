import json
from pathlib import Path

import streamlit as st


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
        st.subheader("You've told us...")

        # Group selected symptoms by category
        grouped = {}
        for entry in patient_context["symptoms"]:
            cat = entry.get("category", "Other")
            grouped.setdefault(cat, []).append(entry)

        for cat, items in grouped.items():
            symptom_lines = [f"{i['symptom']} (severity {i['severity']}/5, {i['duration']})" for i in items]
            st.markdown(f"**{cat}:** {', '.join(symptom_lines)}")

        # Impact
        if patient_context["impact"]:
            st.markdown(f"**Impact:** {', '.join(patient_context['impact'])}")
        else:
            st.markdown("**Impact:** Not specified")

        # Main concern
        if patient_context.get("main_concern"):
            st.markdown("**Main concern:**")
            st.write(patient_context["main_concern"])
        else:
            st.markdown("**Main concern:** Not specified")

        # Appointment goal with added confirmation
        if patient_context.get("appointment_goal"):
            st.markdown("**Appointment goal:**")
            st.write(patient_context["appointment_goal"])
            st.markdown("✅ Added")
        else:
            st.markdown("**Appointment goal:** Not added")

        # Additional notes with confirmation
        if patient_context.get("additional_notes"):
            st.markdown("**Additional notes:**")
            st.write(patient_context["additional_notes"])
            st.markdown("✅ Added")
        else:
            st.markdown("**Additional notes:** Not added")

        # Save this check-in to the logged-in user's account.
        st.divider()
        if username:
            if st.button("Save my progress to my account"):
                save_user_progress(username, patient_context)
                st.success("Progress saved to your account")
        else:
            st.info("Log in to save your progress to your account.")

    return patient_context
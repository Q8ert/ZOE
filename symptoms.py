import streamlit as st

MENOPAUSE_SYMPTOMS = [
    "Hot flushes",
    "Night sweats",
    "Sleep problems",
    "Fatigue",
    "Brain fog",
    "Memory problems",
    "Low mood",
    "Anxiety",
    "Irritability",
    "Joint pain",
    "Headaches",
    "Palpitations",
    "Irregular periods",
    "Heavy periods",
    "Vaginal dryness",
    "Low libido",
    "Digestive changes",
    "Weight changes",
    "Skin changes",
    "Hair changes",
    "Urinary symptoms",
    "Other",
]


def symptom_tracker():
    """Display the symptom check-in form and return the user's context."""

    st.header("Symptom check-in")

    with st.form("symptom_form"):
        symptoms = st.multiselect(
            "Which symptoms are you experiencing?",
            MENOPAUSE_SYMPTOMS,
        )

        other_symptom = ""
        if "Other" in symptoms:
            other_symptom = st.text_input(
                "Please describe the other symptom"
            )

        top_concerns = st.multiselect(
            "Which 1–3 symptoms are affecting you most right now?",
            MENOPAUSE_SYMPTOMS,
            max_selections=3,
        )

        severity = st.slider(
            "Overall, how disruptive are these symptoms right now?",
            0,
            10,
            5,
        )

        duration = st.selectbox(
            "How long has this been going on?",
            [
                "Today",
                "A few days",
                "A few weeks",
                "A few months",
                "Longer than 6 months",
                "Not sure",
            ],
        )

        impact = st.multiselect(
            "What is this affecting?",
            [
                "Sleep",
                "Work or study",
                "Mood",
                "Relationships",
                "Exercise or movement",
                "Caring responsibilities",
                "Daily tasks",
                "Confidence",
            ],
        )

        notes = st.text_area(
            "Anything else you'd like to add?",
            placeholder="Patterns, triggers, what you've tried, worries, previous GP conversations...",
        )

        submitted = st.form_submit_button("Save check-in")

    if submitted:
        clean_symptoms = [s for s in symptoms if s != "Other"]

        if other_symptom:
            clean_symptoms.append(other_symptom)

        patient_context = {
            "symptoms": clean_symptoms,
            "top_concerns": top_concerns,
            "severity": severity,
            "duration": duration,
            "impact": impact,
            "notes": notes,
        }

        st.session_state["patient_context"] = patient_context

        st.success("Check-in saved")

    patient_context = st.session_state.get("patient_context")

    if patient_context:
        st.subheader("Your check-in summary")

        st.write(f"**Symptoms logged:** {len(patient_context['symptoms'])}")

        st.write(
            "**Top concerns:** "
            + (
                ", ".join(patient_context["top_concerns"])
                if patient_context["top_concerns"]
                else "Not selected"
            )
        )

        st.write(f"**Severity:** {patient_context['severity']}/10")
        st.write(f"**Duration:** {patient_context['duration']}")

        st.write(
            "**Impact:** "
            + (
                ", ".join(patient_context["impact"])
                if patient_context["impact"]
                else "Not specified"
            )
        )

    return patient_context

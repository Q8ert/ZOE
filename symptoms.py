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
]


DURATION_OPTIONS = [
    "Not selected",
    "Today",
    "A few days",
    "A few weeks",
    "A few months",
    "Longer than 6 months",
    "Not sure",
]


def symptom_tracker():
    st.header("Symptom check-in")

    st.write(
        "Rate any symptoms you're experiencing. "
        "Leave symptoms at 0 if they don't apply."
    )

    with st.form("symptom_form"):
        symptom_entries = []

        for symptom in MENOPAUSE_SYMPTOMS:
            col1, col2, col3 = st.columns([2, 1, 1.5])

            with col1:
                st.write(symptom)

            with col2:
                severity = st.slider(
                    "Severity",
                    0,
                    5,
                    0,
                    key=f"{symptom}_severity",
                    label_visibility="collapsed",
                )

            with col3:
                duration = st.selectbox(
                    "Duration",
                    DURATION_OPTIONS,
                    key=f"{symptom}_duration",
                    label_visibility="collapsed",
                )

            if severity > 0:
                symptom_entries.append(
                    {
                        "symptom": symptom,
                        "severity": severity,
                        "duration": duration,
                    }
                )

        notes = st.text_area(
            "Anything else you'd like to add?",
            placeholder="Patterns, triggers, what you've tried, worries, previous GP conversations...",
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
            "notes": notes,
        }

        st.session_state["patient_context"] = patient_context
        st.success("Check-in saved")

    patient_context = st.session_state.get("patient_context")

    if patient_context:
        st.subheader("Your check-in summary")

        st.write(f"**Symptoms logged:** {len(patient_context['symptoms'])}")

        st.write("**Top concerns:**")
        for item in patient_context["top_concerns"]:
            st.write(
                f"- {item['symptom']} — severity {item['severity']}/5, {item['duration']}"
            )

        if patient_context["notes"]:
            st.write("**Notes:**")
            st.write(patient_context["notes"])

    return patient_context

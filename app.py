import streamlit as st
from symptoms import symptom_tracker
from reports import create_gp_report, create_in_the_moment_support

st.set_page_config(page_title="Symptom Ally", page_icon="🌿")

st.title("Symptom Ally")
st.write("Track what you're experiencing and turn it into practical support.")

patient_context = symptom_tracker()

if patient_context:
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Get support for right now"):
            support = create_in_the_moment_support(patient_context)
            st.session_state["support"] = support

    with col2:
        if st.button("Generate GP report"):
            gp_report = create_gp_report(patient_context)
            st.session_state["gp_report"] = gp_report

    if "support" in st.session_state:
        st.subheader("Support for right now")
        st.markdown(st.session_state["support"])

    if "gp_report" in st.session_state:
        st.subheader("GP appointment report")
        st.markdown(st.session_state["gp_report"])

        st.download_button(
            "Download GP report",
            data=st.session_state["gp_report"],
            file_name="gp_report.md",
            mime="text/markdown",
        )

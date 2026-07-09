import streamlit as st


BLOG_POSTS = [
    {
        "title": "Why tracking symptoms can help you feel more prepared",
        "category": "Appointment prep",
        "read_time": "3 min read",
        "summary": "A simple guide to noticing patterns before speaking to your GP.",
        "content": """
Tracking symptoms is not about proving that something is wrong. It is about helping you explain what has been happening clearly.

When symptoms happen over days, weeks, or months, it can be difficult to remember the details during an appointment. A short symptom log can help you notice:

- which symptoms are happening most often
- how intense they feel
- how long they have been going on
- how they affect sleep, work, study, relationships, or confidence

You do not need perfect notes. Even a few clear examples can make the conversation easier.

Before your appointment, it may help to bring a short summary of what you have noticed and the questions you want to ask.
""",
    },
    {
        "title": "How to talk to your GP when you feel dismissed",
        "category": "Self-advocacy",
        "read_time": "4 min read",
        "summary": "Gentle ways to make sure your concerns are heard.",
        "content": """
It can feel difficult to explain symptoms when you are worried you will not be taken seriously.

A useful approach is to be specific about the impact. Instead of only saying "I feel tired", you might say:

- "I am struggling to get through work or study."
- "My sleep has changed and it is affecting my mood."
- "These symptoms are affecting my daily life."

You can also ask direct questions, such as:

- "What could be causing this?"
- "Are there tests or checks that would be appropriate?"
- "What should I track before a follow-up appointment?"
- "At what point should I come back?"

You deserve to be listened to. Bringing notes can help you stay focused if the appointment feels rushed.
""",
    },
    {
        "title": "What to include in appointment notes",
        "category": "GP notes",
        "read_time": "2 min read",
        "summary": "A quick checklist for preparing useful GP notes.",
        "content": """
Good appointment notes do not need to be long. They should help your GP quickly understand what is happening.

Useful things to include:

- your main symptoms
- how long they have been happening
- which symptoms are most severe
- what makes them better or worse, if anything
- how they affect daily life
- what you are worried about
- what you want from the appointment

You can also include a few questions you want to ask.

The goal is not to diagnose yourself. The goal is to make the conversation clearer and easier.
""",
    },
]


def blog_page():
    st.title("Seen Blog")
    st.write(
        "Plain-English guides to help you understand your symptoms, prepare for "
        "appointments, and feel more confident speaking up."
    )

    st.info(
        "These articles are for general support and appointment preparation only. "
        "They do not replace medical advice."
    )

    selected_title = st.selectbox(
        "Choose an article",
        [post["title"] for post in BLOG_POSTS],
        key="blog_article_select",
    )

    selected_post = next(
        post for post in BLOG_POSTS if post["title"] == selected_title
    )

    st.divider()

    st.caption(f"{selected_post['category']} \u00b7 {selected_post['read_time']}")
    st.header(selected_post["title"])
    st.write(selected_post["summary"])

    st.markdown(selected_post["content"])

    st.divider()

    st.subheader("More from Seen")

    for post in BLOG_POSTS:
        if post["title"] != selected_post["title"]:
            with st.container(border=True):
                st.caption(f"{post['category']} \u00b7 {post['read_time']}")
                st.markdown(f"**{post['title']}**")
                st.write(post["summary"])
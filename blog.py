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


# Link-style buttons (type="tertiary") exist from Streamlit 1.39+. Detect the
# version so we can render the article names as links where supported, and fall
# back to a normal button (still clickable) on older versions.
def _supports_tertiary() -> bool:
    try:
        parts = st.__version__.split(".")
        major, minor = int(parts[0]), int(parts[1])
    except Exception:
        return False
    return (major, minor) >= (1, 39)


_LINK_SUPPORTED = _supports_tertiary()


def _open_article(title):
    # Runs as an on_click callback, i.e. before the script reruns and before the
    # selectbox is created, so it is safe to set the selectbox value here. This
    # is what makes pressing an article name jump to that article, exactly like
    # choosing it from the dropdown.
    st.session_state["blog_article_select"] = title


def blog_page():
    # Style ONLY the article-name links (link-style buttons): lavender,
    # underlined, no box. Scoped to tertiary buttons so normal buttons keep
    # their look.
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] button[kind="tertiary"],
        [data-testid="stAppViewContainer"] [data-testid="stBaseButton-tertiary"] {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            font-weight: 700 !important;
        }
        [data-testid="stAppViewContainer"] button[kind="tertiary"] *,
        [data-testid="stAppViewContainer"] [data-testid="stBaseButton-tertiary"] * {
            color: #8B5FBF !important;         /* lavender link */
            text-decoration: underline !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Seen Blog")
    st.write(
        "Plain-English guides to help you understand your symptoms, prepare for "
        "appointments, and feel more confident speaking up."
    )

    st.info(
        "These articles are for general support and appointment preparation only. "
        "They do not replace medical advice."
    )

    titles = [post["title"] for post in BLOG_POSTS]
    selected_title = st.selectbox(
        "Choose an article",
        titles,
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
                # ONLY the article name is the clickable link. Pressing it opens
                # that article via the on_click callback above.
                if _LINK_SUPPORTED:
                    st.button(
                        post["title"],
                        key=f"goto_{post['title']}",
                        on_click=_open_article,
                        args=(post["title"],),
                        type="tertiary",
                    )
                else:
                    st.button(
                        post["title"],
                        key=f"goto_{post['title']}",
                        on_click=_open_article,
                        args=(post["title"],),
                    )
                st.write(post["summary"])
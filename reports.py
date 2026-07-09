from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

model = init_chat_model(
    "openai:gpt-4.1-mini",
    temperature=0.2,
)


def create_in_the_moment_support(patient_context):
    messages = [
        SystemMessage(
            content="""
You are a supportive health communication assistant.

You do not diagnose.
You do not recommend medication or treatment.
You provide practical, low-risk support someone could try in the moment.
You encourage urgent care if symptoms sound severe, sudden, or dangerous.
Use warm, plain English.
"""
        ),
        HumanMessage(
            content=f"""
Create concise in-the-moment support based on this patient context.

Patient context:
{patient_context}

Return:

## What might help right now
- 3 practical suggestions

## What to notice
- 2 things to keep track of

## When to seek help urgently
- brief safety guidance

Keep it short.
"""
        ),
    ]

    response = model.invoke(messages)
    return response.content


def create_gp_report(patient_context):
    messages = [
        SystemMessage(
            content="""
You are a healthcare communication assistant.

Your job is to help someone prepare for a GP appointment by writing short notes the patient can bring.
Write in the patient's voice using first-person "I" statements (for example: "I am experiencing...", "I would like to discuss...").
Do not write like a clinician — use everyday language.
Do not diagnose, recommend medication, or invent information.
Prioritise the user's top concerns and make the notes concise and easy for a GP to scan.
Include advice to advocate for themselves and ask questions.
Keep the notes under 300 words.
"""
        ),
        HumanMessage(
            content=f"""
Create a short set of notes the patient can bring to their GP from this patient context.

Patient context:
{patient_context}

Return a markdown document written in the patient's voice (use "I" statements). Include:

- A one-line "Reason for appointment" starting with "I am coming because...".
- "Top concerns": 1–3 short bullet points that start with "I am experiencing..." and briefly say why it matters.
- "Symptom overview": one short line noting how many symptoms or categories are involved (do not list everything).
- "Impact on daily life": 1–2 short lines about what is affected.
- "Useful context from my notes": a brief summary using "I" statements drawn from the patient's notes.
- "Questions I want to ask": 3–4 simple, practical questions starting with "I would like to ask...".
- "What I could add": up to 3 concise suggestions of missing info the patient might collect before the appointment.

Keep the language plain, personal, and under 300 words. Do not diagnose, recommend medications, or invent details.
"""
        ),
    ]

    response = model.invoke(messages)
    return response.content


def create_confirmation_summary(patient_context):
    messages = [
        SystemMessage(
            content="""
You are a warm, plain-English assistant who helps people check their appointment notes.

Do not diagnose or give medical advice.
Write to the user directly using "you" (for example: "You seem to be experiencing...").
Be supportive and concise.
"""
        ),
        HumanMessage(
            content=f"""
Create a short confirmation summary for the user based on this patient context.

Patient context:
{patient_context}

Requirements:
- Address the user as "you" (do not use "I").
- Highlight the main symptoms and concerns in plain language.
- Mention impact if provided.
- Mention what the user wants from the appointment if provided.
- Avoid diagnosis, medical advice, or inventing details.
- Keep it warm, concise, and easy to read.
- End the summary with the exact question: "Does this sound right?"

Return only the short paragraph(s) of the confirmation summary.
"""
        ),
    ]

    response = model.invoke(messages)
    return response.content
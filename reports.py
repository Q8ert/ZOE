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

Your job is to help someone prepare for a GP appointment.
Do not diagnose.
Do not invent information.
Prioritise the user's top concerns.
Make the report concise and easy for a GP to scan.
"""
        ),
        HumanMessage(
            content=f"""
Create a GP appointment report from this patient context.

Patient context:
{patient_context}

Return:

## Reason for appointment

## Top concerns
Summarise the top 1–3 symptoms and why they matter.

## Symptom overview
Mention the total number of symptoms logged, but do not list everything unless useful.

## Impact on daily life

## Useful context from notes

## Questions to ask GP
- 4 practical questions

## Missing information to consider adding
- Up to 3 things, only if relevant.

Keep it under 300 words.
"""
        ),
    ]

    response = model.invoke(messages)
    return response.content

# Seen 🌿

**Helping women feel seen, heard and prepared for healthcare conversations.**

Seen is a Streamlit application built during the Women in Tech x ZOE Hackathon.

It helps people experiencing menopause symptoms organise their health information, receive practical support, and prepare for conversations with their GP.

---

## Why We Built Seen

Many women report feeling unheard or dismissed when seeking healthcare. Appointments are short, symptoms are complex, and it can be difficult to explain what has been happening over weeks or months.

Seen helps transform lived experience into clear, actionable information that supports better conversations between patients and healthcare professionals.

---

## Features

- Secure user registration and login
- Guided symptom check-in
- Prioritisation of the symptoms that matter most
- Free-text notes for additional context
- AI-generated support for managing symptoms in the moment
- AI-generated GP appointment summary
- Downloadable GP report

---

## Technology

- Python
- Streamlit
- LangChain
- OpenAI GPT-4.1 Mini
- bcrypt

---

## Project Structure

```
.
├── app.py              # Main application
├── symptoms.py         # Symptom check-in interface
├── reports.py          # LLM prompts and report generation
├── requirements.txt
└── README.md
```

---

## Running the App

Clone the repository:

```bash
git clone https://github.com/Q8ert/ZOE.git
cd Seen
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate (MacBook)
.venv/Scripts/activate (Windows)
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```text
OPENAI_API_KEY=your_api_key_here
```

Run the app:

```bash
streamlit run app.py
```

---

## Future Development

- Personal symptom timeline
- Community insights and shared experiences
- Personalised appointment preparation
- Follow-up reflections after GP appointments
- PDF report export
- Secure cloud authentication
- Longitudinal symptom tracking

---

## Team

Built over two days during the Women in Tech x ZOE Hackathon.

import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="HR Helpdesk AI Assistant",
    page_icon="🧑‍💼",
    layout="centered",
)

domain_information = """
HR HELP DESK INFORMATION

1. Employees are entitled to 12 casual leaves per year.
2. Employees should apply for leave through the employee portal.
3. Casual leave should normally be requested before the planned absence.
4. Work from home requires approval from the reporting manager.
5. Employees must complete the annual performance review process.
6. Salary is credited on the last working day of each month.
7. Employees should update their emergency contact information through the employee portal.
8. Employees can contact HR for questions regarding employee benefits.
9. Medical leave may require supporting documentation.
10. New employees have a probation period of 6 months from their date of joining.
11. Sick leave is capped at 8 days per year and does not carry forward to the next year.
12. Employees are eligible for a laptop and standard IT equipment from their first day.
13. Reimbursement claims must be submitted within 30 days of the expense.
14. The notice period for resignation is 60 days for confirmed employees.
"""


with st.sidebar:
    st.header("⚙️ Settings")

    if GEMINI_API_KEY:
        st.success("Gemini API key loaded.")
    else:
        st.error("Gemini API key not found.")
        st.info("Create a .env file and add:\n\nGEMINI_API_KEY=your_api_key")

    st.markdown("---")

    model_name = st.selectbox(
        "Select Gemini Model",
        ["gemini-3.6-flash", "gemini-3.6-flash-lite"],
        index=0,
    )

    st.markdown("---")
    st.subheader("Domain: HR Helpdesk")

    with st.expander("View Domain Information"):
        st.text(domain_information)

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.subheader("Example Questions")

    example_questions = [
        "How many casual leaves are available?",
        "How do I apply for leave?",
        "Who approves work from home?",
        "When is salary credited?",
        "What is the notice period for resignation?",
        "What is the capital of France?",
    ]

    for example in example_questions:
        if st.button(example, key=f"example_{example}"):
            st.session_state.pending_question = example
            st.rerun()


st.title("🧑‍💼 HR Helpdesk AI Assistant")
st.caption("Domain-specific Generative AI chatbot - Experiment 7")

if not GEMINI_API_KEY:
    st.warning("Gemini API key was not found. Please add GEMINI_API_KEY to your .env file.")
    st.stop()


client = genai.Client(api_key=GEMINI_API_KEY)


def create_system_prompt():
    return f"""
You are a helpful HR Helpdesk AI assistant.

Your domain is HR Helpdesk.

Use ONLY the following domain information when answering questions about HR policies.

================ DOMAIN INFORMATION ================

{domain_information}

======================================================

INSTRUCTIONS:

1. Answer clearly and concisely.
2. Use the domain information when relevant.
3. Do not invent HR policies, rules, benefits, numbers, dates, or other domain-specific information.
4. If the requested information is not available, clearly say:
   "That information is not available in the provided HR information."
5. If the user asks a question unrelated to HR, explain that the information is outside the supplied HR domain.
6. Base your answer on the provided HR information.
7. Do not make up additional company policies.
"""


def generate_answer(question):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=question,
            config={
                "system_instruction": create_system_prompt(),
                "temperature": 0.3,
                "max_output_tokens": 200,
            },
        )
        return response.text.strip()
    except Exception as error:
        return f"⚠️ Gemini API Error\n\n{error}"


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message("user"):
        st.write(message["question"])
    with st.chat_message("assistant"):
        st.write(message["answer"])


pending_question = st.session_state.pop("pending_question", None)
typed_question = st.chat_input("Ask a question about HR policies...")
question = pending_question or typed_question

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = generate_answer(question)
        st.write(answer)

    st.session_state.messages.append({"question": question, "answer": answer})
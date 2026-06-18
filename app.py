import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# -----------------------
# LOAD API KEY
# -----------------------
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY not found. Add it in .env or Streamlit Secrets")
    st.stop()

client = Groq(api_key=api_key)

st.title("🧠 AI Software Engineer Agent (Swaroop-DevAI)")

task = st.text_area("Enter your software task")


# -----------------------
# TOOL 1: PLANNER
# -----------------------
def planner(task):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""
You are a senior software architect.

Break this task into step-by-step development plan.

Task: {task}

Rules:
- No code
- Only steps
- Be clear and structured
"""
        }]
    )
    return response.choices[0].message.content


# -----------------------
# TOOL 2: CODE GENERATOR
# -----------------------
def code_generator(task, plan):
    response = client.chat.completions.create(
     model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""
You are a senior full-stack developer.

Task:
{task}

Plan:
{plan}

Generate COMPLETE working code.

Rules:
- No explanation
- No planning text
- Only final working code
- Ensure code is runnable
"""
        }]
    )
    return response.choices[0].message.content


# -----------------------
# TOOL 3: REVIEWER
# -----------------------
def reviewer(code):
    response = client.chat.completions.create(
     model="llama-3.1-8b-instant",
        messages=[{
            "role": "user",
            "content": f"""
You are a strict senior code reviewer.

Find bugs and improve the code.

IMPORTANT:
- Return ONLY final corrected code
- No explanation

Code:
{code}
"""
        }]
    )
    return response.choices[0].message.content


# -----------------------
# ORCHESTRATOR (AGENT BRAIN)
# -----------------------
def run_agent(task):
    plan = planner(task)
    code = code_generator(task, plan)
    final_code = reviewer(code)
    return final_code


# -----------------------
# STREAMLIT UI
# -----------------------
if st.button("Run AI Agent 🚀"):

    if not task:
        st.warning("Please enter a task")
        st.stop()

    with st.spinner("AI Agent is thinking... 🧠"):

        result = run_agent(task)

    st.subheader("💻 FINAL OUTPUT")
    st.code(result, language="markdown") 
